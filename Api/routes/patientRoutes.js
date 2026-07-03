import express from 'express';
import { getPatients, getPatientDetail, getPatientResultats } from '../controllers/patientController.js';
// ⚠️ Ajustez le chemin d'import ci-dessus pour qu'il corresponde à l'emplacement
// réel de patientController.js, comme dans vos autres fichiers de routes.

const router = express.Router();

router.get('/', getPatients);
router.get('/:id', getPatientDetail);
router.get('/:id/resultats', getPatientResultats);

export default router;
