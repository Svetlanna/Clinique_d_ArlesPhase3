import fs from 'fs';
import path from 'path';
import csvParser from 'csv-parser';
import { pool } from '../config/db.js';
import { recupererDonnees } from '../etl/extract.js';
import { calculerIndicateurs } from '../etl/transform.js';

export const getAllNuits = async () => {
    const [rows] = await pool.execute('SELECT * FROM resultat_nuit');
    return rows;
};

export const updateCommentaire = async (idNuit, commentaire) => {
    await pool.execute(
        'UPDATE resultat_nuit SET commentaire_medical = ? WHERE id_nuit = ?',
        [commentaire, idNuit]
    );
};

export const fetchNuitData = async (idNuit) => {
    const baseDir = 'C:/python-projs/Clinique_d_Arles/server';
    const cheminCsv = path.join(process.cwd(), "raw", "traite", `signal-psg-patient-${idNuit}-nuit-${idNuit}.csv`);
    const dfCapteur = await new Promise((resolve, reject) => {
        if (!fs.existsSync(cheminCsv)) return reject(new Error(`Fichier introuvable`));
        const results = [];
        fs.createReadStream(cheminCsv)
            .pipe(csvParser())
            .on('data', (data) => results.push(data))
            .on('end', () => resolve(results))
            .on('error', reject);
    });
    const [dfEvents] = await pool.execute('SELECT * FROM evenement_respiratoire WHERE id_nuit = ?', [idNuit]);
    const [apnees, hypo, rera, all] = await Promise.all([
        pool.query("CALL sp_compteur_apnees()"),
        pool.query("CALL sp_compteur_hypopnae()"),
        pool.query("CALL sp_compteur_rera()"),
        pool.query("CALL sp_compteur_all()")
    ]);
    return {
        df_capteur: dfCapteur,
        df_events: dfEvents,
        nbapnees: apnees[0][0],
        nbhypopnees: hypo[0][0],
        nbrera: rera[0][0],
        nbr_events: all[0][0]
    };
};

export const getStats = async (id) => {
    const rawData = await recupererDonnees(id);
    return calculerIndicateurs(
        rawData.df_capteur,
        rawData.nbapnees,
        rawData.nbhypopnees,
        rawData.nbrera,
        rawData.nbr_events
    );
};