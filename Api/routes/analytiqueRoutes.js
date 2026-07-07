import express from 'express';
import { validerDiagnosticNuit, importSuiviCpap } from '../controllers/analytiqueController.js';

const router = express.Router();

// POST /api/analytique/resultats-nuit/:id_nuit/valider
// validation du diagnostic -> insertion resultat_nuit + synchro galaxie
// (faits_nuits / dim_patient / dim_nuit / dim_temps).
router.post('/resultats-nuit/:id_nuit/valider', validerDiagnosticNuit);

// POST /api/analytique/cpap/import
// déclenchement du mini ETL CPAP, lecture du CSV de suivi quotidien -> faits_suivi_cpap_jour.
router.post('/cpap/import', importSuiviCpap);

export default router;
