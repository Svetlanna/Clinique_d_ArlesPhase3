import { pool } from '../config/db.js';

export const login = async (req, res) => {
    // Change these to match your frontend input names
    const { mail, password } = req.body;

    if (!mail || !password) {
        return res.status(400).json({ status: 'error', message: 'Login et mot de passe requis' });
    }

    // Now query the DB using these variables
    const [rows] = await pool.query(
        'SELECT * FROM utilisateur WHERE login = ? AND mot_de_passe = ? AND actif = 1',
        [mail, password] // 'mail' corresponds to the DB 'login' column
    );

    if (rows.length === 0) {
        return res.status(401).json({ status: 'error', message: 'Identifiants invalides' });
    }

    res.json({ status: 'success', data: rows[0] });
};