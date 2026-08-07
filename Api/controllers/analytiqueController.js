import { execFile } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ETL_DIR = path.resolve(__dirname, '../../Etl/base-analytique-et-apps-6a4223e2df3b5611041746');
const PYTHON_BIN = path.join(ETL_DIR, '.venv', 'bin', 'python3');

const runPythonScript = (scriptName, args) => new Promise((resolve, reject) => {
    const scriptPath = path.join(ETL_DIR, scriptName);
    execFile(PYTHON_BIN, [scriptPath, ...args], {
        cwd: ETL_DIR,
        env: process.env,
        maxBuffer: 10 * 1024 * 1024,
    }, (error, stdout, stderr) => {
        if (error) {
            const stderrText = (stderr || '').trim();
            try {
                const parsed = JSON.parse(stderrText);
                return reject(new Error(parsed.error || stderrText));
            } catch {
                return reject(new Error(stderrText || error.message));
            }
        }
        try {
            resolve(JSON.parse(stdout));
        } catch {
            reject(new Error('Réponse du script Python invalide (JSON attendu)'));
        }
    });
});

export const getResultatsNuit = async (req, res) => {
    try {
        const args = [];
        if (req.query.id_nuit) args.push('--id_nuit', String(req.query.id_nuit));
        if (req.query.search) args.push('--search', String(req.query.search));
        const data = await runPythonScript('resultats_nuit_cli.py', args);
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getComorbiditesIA = async (req, res) => {
    try {
        const { id_patient, id_nuit } = req.query;
        if (!id_patient && !id_nuit) {
            return res.status(400).json({ status: 'error', message: 'id_patient ou id_nuit requis' });
        }
        const args = [];
        if (id_patient) args.push('--id_patient', String(id_patient));
        if (id_nuit) args.push('--id_nuit', String(id_nuit));
        const data = await runPythonScript('comorbidites_cli.py', args);
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getDashboardAnalytique = async (req, res) => {
    try {
        const args = [];
        if (req.query.id_patient) args.push('--id_patient', String(req.query.id_patient));
        if (req.query.days) args.push('--days', String(req.query.days));
        if (req.query.seuil) args.push('--seuil', String(req.query.seuil));
        const data = await runPythonScript('dashboard_cli.py', args);
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};
