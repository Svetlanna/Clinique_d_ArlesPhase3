import express from 'express';
import { getPatients, getPatientDetail, getPatientResultats } from '../controllers/patientController.js';


const router = express.Router();

router.get('/', getPatients);
router.get('/:id', getPatientDetail);
router.get('/:id/resultats', getPatientResultats);

export default router;
