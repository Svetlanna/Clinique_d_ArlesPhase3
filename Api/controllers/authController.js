import { pool } from '../config/db.js';

export const login = async (req, res) => {
    const { login, password } = req.body;

    if (!login || !password) {
        return res.status(400).json({ status: 'error', message: 'Champs requis manquants' });
    }


    try {
        // La requête est correcte pour votre structure de table actuelle
        const [rows] = await pool.query(
            'SELECT login, mot_de_passe, role FROM utilisateur WHERE login = ? AND actif = 1',
            [login]
        );

        if (rows.length === 0) {
            return res.status(401).json({ status: 'error', message: 'Identifiants invalides' });
        }

        const user = rows[0];

        // Vérification du mot de passe (comparaison simple car vos données sont en clair dans la capture)
        if (password !== user.mot_de_passe) {
            return res.status(401).json({ status: 'error', message: 'Identifiants invalides' });
        }

        // Succès : on renvoie le mail et le rôle
        res.json({
            data: {
                mail: user.login,
                password: user.role
            }
        });
    } catch (error) {
        console.error("Erreur serveur :", error);
        res.status(500).json({ status: 'error', message: 'Erreur interne du serveur' });
    }
};