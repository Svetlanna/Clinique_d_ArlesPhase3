import PDFDocument from 'pdfkit';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DOSSIERS_DIR = path.join(__dirname, '../data/dossiers-patients');
// Courbes générées par l'ETL Python (Etl/etl/load.py -> sauvegarder_resultats).
const COURBES_NUIT_DIR = path.join(__dirname, '../../Etl/outputs');

const formatValeur = (valeur, unite = '') => (valeur === null || valeur === undefined ? 'N/A' : `${valeur}${unite}`);

// Ajoute une page avec la courbe si le PNG existe, sinon ne fait rien
// (les courbes ne sont générées par l'ETL que pour les nuits déjà traitées).
const ajouterCourbeSiPresente = (doc, nomFichier, titre) => {
    const cheminImage = path.join(COURBES_NUIT_DIR, nomFichier);
    if (!fs.existsSync(cheminImage)) return;
    doc.addPage();
    doc.fontSize(13).text(titre, { underline: true });
    doc.moveDown(0.5);
    doc.image(cheminImage, { fit: [500, 350], align: 'center' });
};

// Génère le PDF du dossier patient (identité, nuit étudiée, indicateurs
// cliniques, validation médicale) suite à la validation du diagnostic.
// Retourne le chemin absolu du fichier écrit.
export const genererDossierPatientPdf = ({ patient, nuit, medecinValidateur, indicateurs, severite_iah, commentaire }) => new Promise((resolve, reject) => {
    fs.mkdirSync(DOSSIERS_DIR, { recursive: true });
    const cheminPdf = path.join(DOSSIERS_DIR, `dossier-patient-${patient.id_patient}-nuit-${nuit.id_nuit}.pdf`);

    const doc = new PDFDocument({ margin: 50 });
    const stream = fs.createWriteStream(cheminPdf);
    doc.pipe(stream);

    doc.fontSize(18).text('Dossier patient - Résultats de nuit', { align: 'center' });
    doc.moveDown(1.5);

    doc.fontSize(13).text('Identité du patient', { underline: true });
    doc.fontSize(11);
    doc.text(`Nom : ${patient.nom} ${patient.prenom}`);
    doc.text(`Date de naissance : ${patient.date_naissance}`);
    doc.text(`Sexe : ${patient.sexe}`);
    doc.text(`IMC initial : ${formatValeur(patient.imc_initial)}`);
    doc.text(`Fumeur : ${patient.fumeur ? 'Oui' : 'Non'}${patient.pa_tabac ? ` (${patient.pa_tabac} paquets-année)` : ''}`);
    doc.text(`Profession : ${formatValeur(patient.profession)}`);
    doc.text(`Niveau d'activité : ${formatValeur(patient.niveau_activite)}`);
    doc.moveDown();

    doc.fontSize(13).text('Étude du sommeil', { underline: true });
    doc.fontSize(11);
    doc.text(`Nuit n° ${nuit.id_nuit} - ${nuit.date_nuit}`);
    doc.text(`Type d'étude : ${nuit.type_etude}`);
    doc.text(`Médecin prescripteur : ${nuit.nom_medecin}`);
    doc.text(`Appareil PSG : ${nuit.modele_appareil_psg}`);
    doc.moveDown();

    doc.fontSize(13).text('Indicateurs cliniques', { underline: true });
    doc.fontSize(11);
    doc.text(`IAH : ${formatValeur(indicateurs.iah)} (sévérité : ${severite_iah ?? 'N/A'})`);
    doc.text(`SpO2 min / moy / médiane : ${formatValeur(indicateurs.spo2_min, '%')} / ${formatValeur(indicateurs.spo2_moy, '%')} / ${formatValeur(indicateurs.spo2_mediane, '%')}`);
    doc.text(`Durée hypoxie : ${formatValeur(indicateurs.duree_hypoxie_min, ' min')}`);
    doc.text(`Apnées : ${indicateurs.nb_apnees} (dont ${formatValeur(indicateurs.pct_apnees_centrales, '%')} centrales)`);
    doc.text(`Hypopnées : ${indicateurs.nb_hypopnees}`);
    doc.text(`RERA : ${indicateurs.nb_rera}`);
    doc.text(`Micro-éveils : ${indicateurs.nb_microeveils}`);
    doc.text(`Durée apnée moyenne / max : ${formatValeur(indicateurs.duree_apnee_moy_sec, ' s')} / ${formatValeur(indicateurs.duree_apnee_max_sec, ' s')}`);
    doc.text(`Position dominante : ${formatValeur(indicateurs.position_dominante)}`);
    doc.text(`Ronflements : ${formatValeur(indicateurs.decibels_moy, ' dB moy')} / ${formatValeur(indicateurs.decibels_max, ' dB max')} - ${indicateurs.nb_ronflements_forts} ronflement(s) fort(s)`);
    doc.text(`Durée du sommeil : ${formatValeur(indicateurs.duree_sommeil_min, ' min')}`);
    doc.moveDown();

    doc.fontSize(13).text('Validation médicale', { underline: true });
    doc.fontSize(11);
    doc.text(`Validé par : Dr ${medecinValidateur.prenom} ${medecinValidateur.nom}`);
    doc.text(`Date de validation : ${new Date().toLocaleDateString('fr-FR')}`);
    doc.moveDown(0.5);
    doc.text('Commentaire médical :');
    doc.text(commentaire || 'Aucun commentaire.');

    ajouterCourbeSiPresente(doc, `courbe_spo2_nuit_${nuit.id_nuit}.png`, `Courbe SpO2 - Nuit ${nuit.id_nuit}`);
    ajouterCourbeSiPresente(doc, `courbe_debit_nasal_nuit_${nuit.id_nuit}.png`, `Courbe débit nasal - Nuit ${nuit.id_nuit}`);
    ajouterCourbeSiPresente(doc, `ronflements${nuit.id_nuit}_vs_temps.png`, `Ronflements - Nuit ${nuit.id_nuit}`);

    doc.end();

    stream.on('finish', () => resolve(cheminPdf));
    stream.on('error', reject);
});
