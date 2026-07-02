// nuitRoutes.js
import express from 'express';
// Assurez-vous d'importer updateNuit ici
import { getNuitData, getStats, getAllNuits, updateNuit, updateCommentaire } from "../controllers/nuitController.js";

const router = express.Router();

router.get('/', getAllNuits);
router.get('/:id/run', getNuitData);
router.get('/:id/stats', getStats);
router.patch('/:id/commentaire', updateCommentaire);

// Ajoutez cette ligne pour rendre la route accessible :

router.put('/:id/update', updateNuit);
export default router;