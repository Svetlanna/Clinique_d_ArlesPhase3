import * as cpapModel from '../models/cpapModel.js';


export const getAllCpap = (req, res) => { 
    try {
        const cpap = cpapModel.getAllCpap(); // Pas de 'await' ici
        res.status(200).json({ status: 'success', cpap });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};