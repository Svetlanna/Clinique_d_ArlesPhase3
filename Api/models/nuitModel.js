import fs from 'fs';
import path from 'path';
import csvParser from 'csv-parser';
import { pool } from '../config/db.js';


import { recupererDonnees } from '../etl/extract.js';

import { calculerIndicateurs } from '../etl/transform.js';


export const fetchAllNuitEtude = async () => {
    const [rows] = await pool.query('SELECT * FROM v_nuit_etude');
    return rows;
};

export const fetchNuitData = async (idNuit) => {
    // 1. Lecture CSV

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

    // 2. Accès SQL
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