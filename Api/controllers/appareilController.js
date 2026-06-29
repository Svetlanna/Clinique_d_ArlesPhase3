import * as AppareilModel from '../models/appareilModel.js';

export const getAllAppareils = async (req, res) => {
    try {
        const data = await AppareilModel.getAll();
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getAppareilById = async (req, res) => {
    try {
        const data = await AppareilModel.getById(req.params.id);
        if (!data) return res.status(404).json({ status: 'error', message: 'Appareil introuvable' });
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const createAppareil = async (req, res) => {
    try {
        const insertId = await AppareilModel.create(req.body);
        res.status(201).json({ status: 'success', id_appareil: insertId });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const updateAppareil = async (req, res) => {
    try {
        const affected = await AppareilModel.update(req.params.id, req.body);
        if (!affected) return res.status(404).json({ status: 'error', message: 'Appareil introuvable' });
        res.status(200).json({ status: 'success', message: 'Appareil mis à jour' });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const deleteAppareil = async (req, res) => {
    try {
        const affected = await AppareilModel.remove(req.params.id);
        if (!affected) return res.status(404).json({ status: 'error', message: 'Appareil introuvable' });
        res.status(200).json({ status: 'success', message: 'Appareil supprimé' });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};
