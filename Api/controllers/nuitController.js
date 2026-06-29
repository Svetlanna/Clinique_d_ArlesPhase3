import * as NuitModel from '../models/nuitModel.js';
import { pool } from '../config/db.js';
export const runNuit = async (req, res) => {
    try {
        const data = await NuitModel.fetchNuitData(req.params.id);
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getNuitData = async (req, res) => {
    try {
        const data = await NuitModel.fetchNuitData(req.params.id);
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getStats = async (req, res) => {
    try {
        const stats = await NuitModel.getStats(req.params.id);
        res.status(200).json({ status: 'success', id_nuit: req.params.id, indicateurs: stats });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};


export const medecineRoute = async (req, res) => {
    try {
        const rows = await medecine();
        res.status(200).json({ status: 'success', count: rows.length, data: rows });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const medecine = async () => {
    const [rows] = await pool.execute(`
        SELECT
            p.id_personnel,
            p.nom,
            p.prenom,
            p.telephone,
            p.email,
            p.date_embauche,
            p.actif,
            m.specialite,
            m.numero_rpps
        FROM medecin m
        JOIN personnel p ON m.id_personnel = p.id_personnel
        ORDER BY p.nom, p.prenom
    `);
    return rows;
};

export const getMedecinById = async (req, res) => {
    try {
        const [rows] = await pool.execute(`
            SELECT
                p.id_personnel,
                p.nom,
                p.prenom,
                p.telephone,
                p.email,
                p.date_embauche,
                p.actif,
                m.specialite,
                m.numero_rpps
            FROM medecin m
            JOIN personnel p ON m.id_personnel = p.id_personnel
            WHERE m.id_personnel = ?
        `, [req.params.id]);
        if (!rows[0]) return res.status(404).json({ status: 'error', message: 'Médecin non trouvé' });
        res.status(200).json({ status: 'success', data: rows[0] });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};