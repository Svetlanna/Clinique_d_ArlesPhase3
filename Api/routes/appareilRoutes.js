import express from 'express';
import { getAllAppareils, getAppareilById, createAppareil, updateAppareil, deleteAppareil } from '../controllers/appareilController.js';

const router = express.Router();

router.get('/', getAllAppareils);
router.get('/:id', getAppareilById);
router.post('/', createAppareil);
router.put('/:id', updateAppareil);
router.delete('/:id', deleteAppareil);

export default router;
