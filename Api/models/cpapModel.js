import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const filename = fileURLToPath(import.meta.url);
const dirname = path.dirname(filename);

const db = new Database(path.join(dirname, '../../base_analytique.db'));

export const getAllCpap = () => {
const rows = db.prepare('SELECT * FROM faits_suivi_cpap_jour').all();
return rows;
}