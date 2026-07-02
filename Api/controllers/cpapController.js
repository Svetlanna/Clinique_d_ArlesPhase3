import * as cpapModel from '../models/cpapModel.js';


export const getAllCpap = async (req, res) => {
    try {
        const cpap = await cpapModel.getAllCpap();
        res.status(200).json({ status: 'success', cpap});
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};
