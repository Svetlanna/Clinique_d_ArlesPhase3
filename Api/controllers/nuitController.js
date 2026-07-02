import * as NuitModel from '../models/nuitModel.js';
import { pool } from '../config/db.js';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// Définition des chemins globaux (sûr pour ES Modules)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


export const runNuit = async (req, res) => {
    try {
        const data = await NuitModel.fetchNuitData(req.params.id);
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getAllNuitEtude = async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM v_nuit_etude');
        res.status(200).json({ status: 'success', count: rows.length, data: rows });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getAllNuits = async (req, res) => {
    try {
        const nuits = await NuitModel.getAllNuits();
        res.status(200).json({ status: 'success', data: nuits });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

// Mettre à jour le commentaire
export const updateCommentaire = async (req, res) => {
    try {
        const idNuit = req.params.id;
        const commentaire = req.body.commentaire;
        await NuitModel.updateCommentaire(idNuit, commentaire);
        res.status(200).json({ status: 'success', data: { idNuit, commentaire } });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

// Assigner un médecin
export const assignMedecin = async (req, res) => {
    const { id } = req.params;
    const { idMedecin } = req.body;
    await pool.execute('UPDATE nuit_etude SET id_medecin = ? WHERE id_nuit = ?', [idMedecin, id]);
    res.status(200).json({ status: 'success' });
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


export const updateNuit = async (req, res) => {
    const { id } = req.params;
    const { commentaire, idMedecin } = req.body;

    const scriptPath = path.join(__dirname, "..", "..", "Etl", "index.py");
    const args = [
        scriptPath,
        "update",
        String(commentaire || ""),
        String(idMedecin || ""),
        String(id)
    ];

const pythonExecutable = process.env.PYTHON_PATH || "python";
const pythonProcess = spawn(pythonExecutable, args);
    let errorOutput = '';

    pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
        console.error(`ERREUR PYTHON : ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            // Succès
            res.status(200).json({ status: 'success', message: 'Mise à jour effectuée' });
        } else {
            // En cas d'erreur côté Python, on renvoie les détails
            res.status(500).json({
                status: 'error',
                message: 'Erreur exécution Python',
                details: errorOutput
            });
        }
    });
};