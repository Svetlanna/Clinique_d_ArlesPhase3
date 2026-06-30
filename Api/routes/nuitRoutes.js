// nuitRoutes.js
import express from 'express';
// Assurez-vous d'importer updateNuit ici
import { getNuitData, getStats, getAllNuitEtude, updateNuit } from "../controllers/nuitController.js";

const router = express.Router();

router.get('/', getAllNuitEtude);
router.get('/:id/run', getNuitData);
router.get('/:id/stats', getStats);

// Ajoutez cette ligne pour rendre la route accessible :

router.put('/:id/update', updateNuit);
export default router;