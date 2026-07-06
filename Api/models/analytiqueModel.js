import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';
import { upsertDimTemps, upsertDimPatient, upsertDimNuit } from './galaxieDimensions.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Galaxie SQLite "racine", celle utilisée par les apps Streamlit de Etl/
// (app_resultats_nuit_avec_ia.py, ia_comorbidites.py) pour l'entraînement IA.
const db = new Database(path.join(__dirname, '../../base_analytique.db'));

export const computeSeveriteIah = (iah) => {
    if (iah === null || iah === undefined) return null;
    if (iah < 5) return 'normal';
    if (iah < 15) return 'léger';
    if (iah < 30) return 'modéré';
    return 'sévère';
};

// Insère/actualise la nuit dans la galaxie : dim_patient, dim_nuit, dim_temps
// puis faits_nuits.
export const syncNuitDansGalaxie = ({ patient, nuit, indicateurs }) => {
    const id_temps = upsertDimTemps(db, nuit.date_nuit);

    upsertDimPatient(db, {
        id_patient: patient.id_patient,
        nom: patient.nom,
        prenom: patient.prenom,
        date_naissance: patient.date_naissance,
        sexe: patient.sexe,
        imc_initial: patient.imc_initial,
        fumeur_initial: patient.fumeur,
        pa_tabac_initial: patient.pa_tabac,
        profession: patient.profession,
        niveau_activite: patient.niveau_activite,
        date_maj: new Date().toISOString().slice(0, 10),
    });

    upsertDimNuit(db, {
        id_nuit: nuit.id_nuit,
        date_nuit: nuit.date_nuit,
        type_etude: nuit.type_etude,
        nom_medecin: nuit.nom_medecin,
        modele_appareil_psg: nuit.modele_appareil_psg,
    });

    db.prepare(`
        INSERT INTO faits_nuits (
            id_nuit, id_patient, id_temps,
            iah, severite_iah, spo2_min, spo2_moy, spo2_mediane,
            nb_apnees, nb_hypopnees, nb_rera, nb_microeveils,
            duree_sommeil_min, duree_hypoxie_min, position_dominante,
            decibels_max, decibels_moy, nb_ronflements_forts,
            id_suivi_le_plus_proche, pct_apnees_centrales
        ) VALUES (
            @id_nuit, @id_patient, @id_temps,
            @iah, @severite_iah, @spo2_min, @spo2_moy, @spo2_mediane,
            @nb_apnees, @nb_hypopnees, @nb_rera, @nb_microeveils,
            @duree_sommeil_min, @duree_hypoxie_min, @position_dominante,
            @decibels_max, @decibels_moy, @nb_ronflements_forts,
            @id_suivi_le_plus_proche, @pct_apnees_centrales
        )
        ON CONFLICT(id_nuit) DO UPDATE SET
            id_patient = excluded.id_patient,
            id_temps = excluded.id_temps,
            iah = excluded.iah,
            severite_iah = excluded.severite_iah,
            spo2_min = excluded.spo2_min,
            spo2_moy = excluded.spo2_moy,
            spo2_mediane = excluded.spo2_mediane,
            nb_apnees = excluded.nb_apnees,
            nb_hypopnees = excluded.nb_hypopnees,
            nb_rera = excluded.nb_rera,
            nb_microeveils = excluded.nb_microeveils,
            duree_sommeil_min = excluded.duree_sommeil_min,
            duree_hypoxie_min = excluded.duree_hypoxie_min,
            position_dominante = excluded.position_dominante,
            decibels_max = excluded.decibels_max,
            decibels_moy = excluded.decibels_moy,
            nb_ronflements_forts = excluded.nb_ronflements_forts,
            pct_apnees_centrales = excluded.pct_apnees_centrales
    `).run({
        id_patient: patient.id_patient,
        id_temps,
        id_suivi_le_plus_proche: null,
        ...indicateurs,
        id_nuit: nuit.id_nuit,
        severite_iah: computeSeveriteIah(indicateurs.iah),
    });

    return { id_temps };
};
