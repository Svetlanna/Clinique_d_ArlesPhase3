import express from 'express';
import {
    getResultatsNuit,
    getComorbiditesIA,
    getDashboardAnalytique,
    validerDiagnosticNuit,
    importSuiviCpap,
} from '../controllers/analytiqueController.js';

const router = express.Router();

// GET /api/analytique/resultats-nuit?id_nuit=&search=
router.get('/resultats-nuit', getResultatsNuit);

// GET /api/analytique/comorbidites?id_patient=&id_nuit=
router.get('/comorbidites', getComorbiditesIA);

// GET /api/analytique/dashboard?id_patient=&days=&seuil=
router.get('/dashboard', getDashboardAnalytique);

// POST /api/analytique/resultats-nuit/:id_nuit/valider
// validation du diagnostic -> PDF + insertion faits_nuits / dim_patient / dim_nuit / dim_temps.
router.post('/resultats-nuit/:id_nuit/valider', validerDiagnosticNuit);

// POST /api/analytique/cpap/import
// déclenchement du mini ETL CPAP, lecture du CSV de suivi quotidien -> faits_suivi_cpap_jour.
router.post('/cpap/import', importSuiviCpap);

export default router;
