// routes/nuitRoutes.js

import express from 'express';
// AJOUTEZ getAllNuits dans la liste des imports ci-dessous :
import {
    getNuitData,
    getStats,
    getAllNuitEtude,
    updateNuit,
    getAllNuits,
    updateCommentaire
} from "../controllers/nuitController.js";

const router = express.Router();

// Maintenant, cette ligne fonctionnera car getAllNuits est importé
router.get('/all', getAllNuits);
router.patch('/:id/commentaire', updateCommentaire);
router.get('/', getAllNuitEtude);
router.get('/:id/run', getNuitData);
router.get('/:id/stats', getStats);
router.put('/:id/update', updateNuit);

export default router;