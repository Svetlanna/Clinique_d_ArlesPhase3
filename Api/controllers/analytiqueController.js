import fs from 'fs';
import path from 'path';
import csvParser from 'csv-parser';
import { pool } from '../config/db.js';
import { syncNuitDansGalaxie, computeSeveriteIah } from '../models/analytiqueModel.js';
import { toDateStr } from '../models/galaxieDimensions.js';
import { importCsvSuiviCpap } from '../models/cpapModel.js';

const lireCapteursNuit = (idPatient, idNuit) => new Promise((resolve, reject) => {
    const cheminCsv = path.join(process.cwd(), 'raw', 'traite', `signal-psg-patient-${idPatient}-nuit-${idNuit}.csv`);
    if (!fs.existsSync(cheminCsv)) {
        return reject(new Error(`Fichier capteurs introuvable : ${cheminCsv}`));
    }
    const rows = [];
    fs.createReadStream(cheminCsv)
        .pipe(csvParser())
        .on('data', (row) => rows.push(row))
        .on('end', () => resolve(rows))
        .on('error', reject);
});

const median = (values) => {
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};

const mode = (values) => {
    const counts = values.reduce((acc, v) => { acc[v] = (acc[v] || 0) + 1; return acc; }, {});
    return Object.keys(counts).reduce((a, b) => (counts[a] > counts[b] ? a : b), 'inconnue');
};

// Calcule les indicateurs cliniques d'une nuit à partir des capteurs 
// et des événements respiratoires MySQL.
// evenement_respiratoire filtré par id_nuit plutôt que les procédures stockées
// sp_compteur_* (celles-ci comptent sur TOUTE la table, sans filtre id_nuit).
const calculerIndicateursNuit = async (idPatient, idNuit) => {
    const capteurs = await lireCapteursNuit(idPatient, idNuit);
    const spo2 = capteurs.map((r) => parseFloat(r.spo2) || 0);
    const decibels = capteurs.map((r) => parseFloat(r.ronflements_db) || 0);
    const positions = capteurs.map((r) => r.position);

    const [evenements] = await pool.execute(
        'SELECT type_evenement, COUNT(*) AS total FROM evenement_respiratoire WHERE id_nuit = ? GROUP BY type_evenement',
        [idNuit]
    );
    const compteParType = Object.fromEntries(evenements.map((e) => [e.type_evenement, e.total]));
    const nbApneesObstructives = compteParType['apnée obstructive'] || 0;
    const nbApneesCentrales = compteParType['apnée centrale'] || 0;
    const nb_apnees = nbApneesObstructives + nbApneesCentrales;
    const nb_hypopnees = compteParType['hypopnée'] || 0;
    const nb_rera = compteParType['RERA'] || 0;

    const [[dureeApnees]] = await pool.query(
        `SELECT AVG(duree_sec) AS moy, MAX(duree_sec) AS max
         FROM evenement_respiratoire
         WHERE id_nuit = ? AND type_evenement IN ('apnée obstructive', 'apnée centrale')`,
        [idNuit]
    );

    const duree_sommeil_min = Math.round(capteurs.length * (10 / 60));
    const iah = duree_sommeil_min > 0 ? (nb_apnees + nb_hypopnees) / (duree_sommeil_min / 60) : null;

    return {
        iah: iah !== null ? Number(iah.toFixed(1)) : null,
        spo2_min: Math.min(...spo2),
        spo2_moy: Number((spo2.reduce((a, b) => a + b, 0) / spo2.length).toFixed(1)),
        spo2_mediane: median(spo2),
        nb_apnees,
        nb_hypopnees,
        nb_rera,
        nb_microeveils: 0,
        duree_sommeil_min,
        duree_hypoxie_min: Number((spo2.filter((s) => s < 90).length * (10 / 60)).toFixed(1)),
        position_dominante: mode(positions),
        duree_apnee_moy_sec: dureeApnees.moy !== null ? Math.round(dureeApnees.moy) : null,
        duree_apnee_max_sec: dureeApnees.max,
        decibels_max: Math.max(...decibels),
        decibels_moy: Number((decibels.reduce((a, b) => a + b, 0) / decibels.length).toFixed(1)),
        nb_ronflements_forts: decibels.filter((d) => d > 70).length,
        pct_apnees_centrales: nb_apnees > 0 ? Number(((nbApneesCentrales / nb_apnees) * 100).toFixed(1)) : null,
    };
};

// Validation du diagnostic par le médecin :
// génère le PDF complet dans le dossier patient, insère/actualise la ligne
// dans resultat_nuit (MySQL), puis synchronise faits_nuits / dim_patient /
// dim_nuit / dim_temps dans la galaxie SQLite.
export const validerDiagnosticNuit = async (req, res) => {
    const id_nuit = Number(req.params.id_nuit);
    const { id_medecin_validateur, commentaire } = req.body || {};

    if (!id_medecin_validateur) {
        return res.status(400).json({ status: 'error', message: 'id_medecin_validateur requis' });
    }

    try {
        const [[nuit]] = await pool.execute(
            `SELECT n.id_nuit, n.date_nuit, n.type_etude, n.id_patient,
                    p.nom, p.prenom, p.date_naissance, p.sexe, p.imc_initial,
                    p.fumeur, p.pa_tabac, p.profession, p.niveau_activite,
                    pm.nom AS medecin_nom, pm.prenom AS medecin_prenom,
                    a.modele AS appareil_modele
             FROM nuit_etude n
             JOIN patient p ON p.id_patient = n.id_patient
             JOIN medecin m ON m.id_personnel = n.id_medecin
             JOIN personnel pm ON pm.id_personnel = m.id_personnel
             JOIN appareil a ON a.id_appareil = n.id_appareil_psg
             WHERE n.id_nuit = ?`,
            [id_nuit]
        );
        if (!nuit) {
            return res.status(404).json({ status: 'error', message: 'Nuit introuvable' });
        }

        const [[medecinValidateur]] = await pool.execute(
            `SELECT pm.nom, pm.prenom FROM medecin m
             JOIN personnel pm ON pm.id_personnel = m.id_personnel
             WHERE m.id_personnel = ?`,
            [id_medecin_validateur]
        );
        if (!medecinValidateur) {
            return res.status(400).json({ status: 'error', message: 'Médecin validateur introuvable' });
        }

        const indicateurs = await calculerIndicateursNuit(nuit.id_patient, id_nuit);
        const severite_iah = computeSeveriteIah(indicateurs.iah);

        let commentaireFinal = commentaire;
        if (commentaireFinal === undefined) {
            const [[existant]] = await pool.execute(
                'SELECT commentaire_medical FROM resultat_nuit WHERE id_nuit = ?',
                [id_nuit]
            );
            commentaireFinal = existant ? existant.commentaire_medical : null;
        }

        await pool.execute(
            `INSERT INTO resultat_nuit (
                id_nuit, id_medecin_validateur, date_validation,
                iah, spo2_min, spo2_moy, spo2_mediane,
                nb_apnees, nb_hypopnees, nb_rera, nb_microeveils,
                duree_sommeil_min, duree_hypoxie_min, position_dominante,
                duree_apnee_moy_sec, duree_apnee_max_sec,
                decibels_max, decibels_moy, nb_ronflements_forts,
                commentaire_medical
            ) VALUES (?, ?, CURDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                id_medecin_validateur = VALUES(id_medecin_validateur),
                date_validation = VALUES(date_validation),
                iah = VALUES(iah), spo2_min = VALUES(spo2_min), spo2_moy = VALUES(spo2_moy),
                spo2_mediane = VALUES(spo2_mediane), nb_apnees = VALUES(nb_apnees),
                nb_hypopnees = VALUES(nb_hypopnees), nb_rera = VALUES(nb_rera),
                nb_microeveils = VALUES(nb_microeveils), duree_sommeil_min = VALUES(duree_sommeil_min),
                duree_hypoxie_min = VALUES(duree_hypoxie_min), position_dominante = VALUES(position_dominante),
                duree_apnee_moy_sec = VALUES(duree_apnee_moy_sec), duree_apnee_max_sec = VALUES(duree_apnee_max_sec),
                decibels_max = VALUES(decibels_max), decibels_moy = VALUES(decibels_moy),
                nb_ronflements_forts = VALUES(nb_ronflements_forts), commentaire_medical = VALUES(commentaire_medical)`,
            [
                id_nuit, id_medecin_validateur,
                indicateurs.iah, indicateurs.spo2_min, indicateurs.spo2_moy, indicateurs.spo2_mediane,
                indicateurs.nb_apnees, indicateurs.nb_hypopnees, indicateurs.nb_rera, indicateurs.nb_microeveils,
                indicateurs.duree_sommeil_min, indicateurs.duree_hypoxie_min, indicateurs.position_dominante,
                indicateurs.duree_apnee_moy_sec, indicateurs.duree_apnee_max_sec,
                indicateurs.decibels_max, indicateurs.decibels_moy, indicateurs.nb_ronflements_forts,
                commentaireFinal,
            ]
        );

        const patient = {
            id_patient: nuit.id_patient, nom: nuit.nom, prenom: nuit.prenom,
            date_naissance: toDateStr(nuit.date_naissance), sexe: nuit.sexe, imc_initial: nuit.imc_initial,
            fumeur: nuit.fumeur, pa_tabac: nuit.pa_tabac, profession: nuit.profession,
            niveau_activite: nuit.niveau_activite,
        };
        const nuitInfo = {
            id_nuit: nuit.id_nuit, date_nuit: toDateStr(nuit.date_nuit), type_etude: nuit.type_etude,
            nom_medecin: `${nuit.medecin_prenom} ${nuit.medecin_nom}`,
            modele_appareil_psg: nuit.appareil_modele,
        };

        const galaxie = syncNuitDansGalaxie({ patient, nuit: nuitInfo, indicateurs });

        res.status(200).json({
            status: 'success',
            data: { id_nuit, indicateurs: { ...indicateurs, severite_iah }, galaxie },
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

// mini ETL CPAP : lit le CSV de suivi 
// quotidien et insère dans faits_suivi_cpap_jour avec calcul des alertes
// (observance < 4h, IAH résiduel > 5).
export const importSuiviCpap = async (req, res) => {
    const body = req.body || {};
    const id_patient = Number(body.id_patient ?? 1);
    const id_appareil = Number(body.id_appareil ?? 1);

    try {
        const resultat = await importCsvSuiviCpap({ id_patient, id_appareil });
        res.status(200).json({ status: 'success', data: resultat });
    } catch (error) {
        const notFound = /introuvable|ENOENT/i.test(error.message);
        res.status(notFound ? 404 : 500).json({ status: 'error', message: error.message });
    }
};
