import { pool } from '../config/db.js';

export const getAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM appareil');
    return rows;
};

export const getById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM appareil WHERE id_appareil = ?', [id]);
    return rows[0] || null;
};

export const create = async ({ modele, numero_serie, fabricant, date_installation, statut, localisation }) => {
    const [result] = await pool.execute(
        'INSERT INTO appareil (modele, numero_serie, fabricant, date_installation, statut, localisation) VALUES (?, ?, ?, ?, ?, ?)',
        [modele, numero_serie ?? null, fabricant ?? null, date_installation ?? null, statut ?? 'actif', localisation ?? null]
    );
    return result.insertId;
};

export const update = async (id, { modele, numero_serie, fabricant, date_installation, statut, localisation }) => {
    const [result] = await pool.execute(
        'UPDATE appareil SET modele = ?, numero_serie = ?, fabricant = ?, date_installation = ?, statut = ?, localisation = ? WHERE id_appareil = ?',
        [modele, numero_serie ?? null, fabricant ?? null, date_installation ?? null, statut, localisation ?? null, id]
    );
    return result.affectedRows;
};

export const remove = async (id) => {
    const [result] = await pool.execute('DELETE FROM appareil WHERE id_appareil = ?', [id]);
    return result.affectedRows;
};
