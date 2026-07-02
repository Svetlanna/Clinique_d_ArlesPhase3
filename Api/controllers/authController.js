import { pool } from '../config/db.js';

export const login = async (req, res) => {
    console.log('Body reçu :', req.body);
    const { login: identifiant, password } = req.body;

    if (!identifiant || !password) {
        return res.status(400).json({ status: 'error', message: 'Login et mot de passe requis' });
    }

    try {
        const [rows] = await pool.query(
            'SELECT * FROM utilisateur WHERE login = ? AND mot_de_passe = ? AND actif = 1',
            [identifiant, password]
        );

        if (rows.length === 0) {
            return res.status(401).json({ status: 'error', message: 'Identifiants invalides' });
        }

        res.json({ status: 'success', data: rows[0] });

    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};