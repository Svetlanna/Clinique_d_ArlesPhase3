import { pool } from '../config/db.js';

export const getAllCpap = async() => {
const [rows] = (await pool.execute('SELECT * FROM suivi_cpapjour'));
return rows;
}