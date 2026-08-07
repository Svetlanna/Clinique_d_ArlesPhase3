import { pool } from '../../../Api/config/db.js';
export const getPatients = async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT p.id_patient,
             CONCAT(p.prenom, ' ', p.nom) AS patient,
             p.date_naissance,
             TIMESTAMPDIFF(YEAR, p.date_naissance, CURDATE()) AS age,
             p.sexe, p.imc_initial, p.profession,
             IF(p.fumeur, 'Oui', 'Non') AS fumeur,
             p.niveau_activite,
             IF(p.actif, 'Actif', 'Inactif') AS statut
      FROM patient p
      ORDER BY p.nom
    `);
    res.json({ status: 'ok', data: rows });
  } catch (error) {
    console.error('Erreur getPatients :', error);
    res.status(500).json({ status: 'error', message: 'Erreur interne du serveur' });
  }
};


export const getPatientDetail = async (req, res) => {
  const { id } = req.params;
  try {
    const [patientRows] = await pool.query(`
      SELECT p.id_patient,
             CONCAT(p.prenom, ' ', p.nom) AS patient,
             p.date_naissance,
             TIMESTAMPDIFF(YEAR, p.date_naissance, CURDATE()) AS age,
             p.sexe, p.imc_initial, p.profession,
             IF(p.fumeur, 'Oui', 'Non') AS fumeur,
             p.niveau_activite,
             IF(p.actif, 'Actif', 'Inactif') AS statut
      FROM patient p WHERE p.id_patient = ?
    `, [id]);

    if (patientRows.length === 0) {
      return res.status(404).json({ status: 'error', message: 'Patient introuvable' });
    }

    const [comorbidites] = await pool.query(`
      SELECT c.libelle, c.categorie, pc.date_diagnostic
      FROM patient_comorbidite pc
      JOIN comorbidite c ON c.id_comorbidite = pc.id_comorbidite
      WHERE pc.id_patient = ?
    `, [id]);

    const [dernierSuivi] = await pool.query(`
      SELECT date_suivi, poids, imc, tension_systolique, tension_diastolique,
             statut_tabac, notes_evolution, statut_patient
      FROM suivi_patient
      WHERE id_patient = ?
      ORDER BY date_suivi DESC LIMIT 1
    `, [id]);

    res.json({
      status: 'ok',
      data: {
        patient: patientRows[0],
        comorbidites,
        dernierSuivi: dernierSuivi[0] ?? null,
      },
    });
  } catch (error) {
    console.error('Erreur getPatientDetail :', error);
    res.status(500).json({ status: 'error', message: 'Erreur interne du serveur' });
  }
};

// GET /api/patient/:id/resultats
// Résultats de nuit d'un patient (équivalent page_resultats() filtré par patient)
export const getPatientResultats = async (req, res) => {
  const { id } = req.params;
  try {
    const [rows] = await pool.query(`
      SELECT n.id_nuit, n.date_nuit,
             CONCAT(per.prenom, ' ', per.nom) AS medecin_validateur,
             r.date_validation, r.iah, r.severite_iah,
             r.spo2_min, r.spo2_moy, r.spo2_mediane,
             r.nb_apnees, r.nb_hypopnees, r.nb_rera, r.nb_microeveils,
             r.duree_sommeil_min, r.duree_hypoxie_min,
             r.position_dominante, r.duree_apnee_moy_sec, r.duree_apnee_max_sec,
             r.decibels_max, r.decibels_moy, r.nb_ronflements_forts,
             r.commentaire_medical
      FROM resultat_nuit r
      JOIN nuit_etude n ON n.id_nuit = r.id_nuit
      JOIN personnel per ON per.id_personnel = r.id_medecin_validateur
      WHERE n.id_patient = ?
      ORDER BY n.date_nuit DESC
    `, [id]);

    res.json({ status: 'ok', data: rows });
  } catch (error) {
    console.error('Erreur getPatientResultats :', error);
    res.status(500).json({ status: 'error', message: 'Erreur interne du serveur' });
  }
};
