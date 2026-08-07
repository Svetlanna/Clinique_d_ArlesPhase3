import express from 'express';
import {
    getResultatsNuit,
    getComorbiditesIA,
    getDashboardAnalytique,
} from '../controllers/analytiqueController.js';

const router = express.Router();

// GET /api/analytique/resultats-nuit?id_nuit=&search=
router.get('/resultats-nuit', getResultatsNuit);

// GET /api/analytique/comorbidites?id_patient=&id_nuit=
router.get('/comorbidites', getComorbiditesIA);

// GET /api/analytique/dashboard?id_patient=&days=&seuil=
router.get('/dashboard', getDashboardAnalytique);

export default router;
