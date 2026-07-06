import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const db = new Database(path.join(__dirname, '../../etl2/base_analytique.db'));

export const getAllCpap = () => {
const rows = db.prepare('SELECT * FROM faits_suivi_cpap_jour').all();
export const getAllCpap = () => {
const rows = db.prepare('SELECT * FROM faits_suivi_cpap_jour').all();
return rows;
}

const lireCsvSuiviCpap = (idPatient, idAppareil) => new Promise((resolve, reject) => {
    const cheminCsv = path.join(RAW_CPAP_DIR, `signal-cpap-patient-${idPatient}-appareil-${idAppareil}.csv`);
    if (!fs.existsSync(cheminCsv)) {
        return reject(new Error(`Fichier CPAP introuvable : ${cheminCsv}`));
    }
    const rows = [];
    fs.createReadStream(cheminCsv)
        .pipe(csvParser())
        .on('data', (row) => rows.push(row))
        .on('end', () => resolve(rows))
        .on('error', reject);
});

// Mini ETL CPAP
export const importCsvSuiviCpap = async ({ id_patient, id_appareil }) => {
    const lignes = await lireCsvSuiviCpap(id_patient, id_appareil);

    const [[suivi]] = await pool.execute(
        'SELECT id_suivi FROM suivi_patient WHERE id_patient = ? ORDER BY date_suivi DESC LIMIT 1',
        [id_patient]
    );
    if (!suivi) {
        throw new Error(`Aucun suivi_patient pour le patient ${id_patient} : impossible de tracer id_suivi_source`);
    }

    const upsertLigne = db.prepare(`
        DELETE FROM faits_suivi_cpap_jour WHERE id_patient = ? AND id_temps = ?
    `);
    const insertLigne = db.prepare(`
        INSERT INTO faits_suivi_cpap_jour (
            id_suivi_source, id_patient, id_temps,
            duree_utilisation_h, iah_residuel, fuites_l_min, nb_evenements, qualite_donnee,
            id_suivi_le_plus_proche, alerte_observance_insuffisante, alerte_iah_eleve
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    let nbAlertesObservance = 0;
    let nbAlertesIah = 0;

    const importerTout = db.transaction((rows) => {
        for (const row of rows) {
            const id_temps = upsertDimTemps(db, row.date);
            const duree_utilisation_h = parseFloat(row.duree_utilisation_heures);
            const iah_residuel = parseFloat(row.iah_residuel);
            const alerte_observance_insuffisante = duree_utilisation_h < 4 ? 1 : 0;
            const alerte_iah_eleve = iah_residuel > 5 ? 1 : 0;

            if (alerte_observance_insuffisante) nbAlertesObservance += 1;
            if (alerte_iah_eleve) nbAlertesIah += 1;

            upsertLigne.run(id_patient, id_temps);
            insertLigne.run(
                suivi.id_suivi, id_patient, id_temps,
                duree_utilisation_h, iah_residuel,
                parseFloat(row.fuite_l_min), parseInt(row.nb_evenements, 10), row.qualite_donnee,
                null, alerte_observance_insuffisante, alerte_iah_eleve
            );
        }
    });
    importerTout(lignes);

    return {
        id_patient,
        id_appareil,
        nb_lignes_traitees: lignes.length,
        nb_alertes_observance: nbAlertesObservance,
        nb_alertes_iah: nbAlertesIah,
    };
};