-- Schéma de la galaxie SQLite (base_analytique.db), racine du projet.
-- base_analytique.db est gitignoré (*.db) : ce fichier est la seule source
-- reproductible du schéma. Exécuté (IF NOT EXISTS) à chaque démarrage de
-- l'API par analytiqueModel.js pour que la base se reconstruise seule sur
-- n'importe quelle machine (fresh clone).

CREATE TABLE IF NOT EXISTS dim_temps (
    id_temps        INTEGER PRIMARY KEY,   -- format AAAAMMJJ, ex: 20240315
    date_complete   TEXT NOT NULL,         -- '2024-03-15'
    annee           INTEGER NOT NULL,
    mois            INTEGER NOT NULL,
    jour            INTEGER NOT NULL,
    trimestre       INTEGER NOT NULL,
    jour_semaine    TEXT NOT NULL,         -- 'lundi', 'mardi', ...
    est_weekend     INTEGER NOT NULL DEFAULT 0  -- 0/1
);

CREATE TABLE IF NOT EXISTS dim_patient (
    id_patient          INTEGER PRIMARY KEY,  -- même id que clinique_v2.patient
    nom                 TEXT NOT NULL,
    prenom              TEXT NOT NULL,
    date_naissance      TEXT NOT NULL,
    sexe                TEXT NOT NULL,
    imc_initial         REAL,
    fumeur_initial      INTEGER,              -- 0/1 au diagnostic
    pa_tabac_initial    INTEGER,
    profession          TEXT,
    niveau_activite     TEXT,
    date_maj            TEXT NOT NULL         -- date de dernière synchro depuis clinique_v2
);

CREATE TABLE IF NOT EXISTS dim_nuit (
    id_nuit             INTEGER PRIMARY KEY,  -- même id que clinique_v2.nuit_etude
    date_nuit           TEXT NOT NULL,
    type_etude          TEXT NOT NULL,        -- polysomnographie / polygraphie / titration CPAP
    nom_medecin         TEXT,
    modele_appareil_psg TEXT
);

CREATE TABLE IF NOT EXISTS dim_comorbidite (
    id_comorbidite      INTEGER PRIMARY KEY,  -- même id que clinique_v2.comorbidite
    libelle             TEXT NOT NULL,
    categorie           TEXT                  -- cardiovasculaire / métabolique / respiratoire / ...
);

CREATE TABLE IF NOT EXISTS dim_suivi_patient (
    id_suivi            INTEGER PRIMARY KEY,  -- même id que clinique_v2.suivi_patient
    id_patient          INTEGER NOT NULL,
    date_suivi          TEXT NOT NULL,
    poids               REAL,
    imc                 REAL,
    tension_systolique  INTEGER,
    tension_diastolique INTEGER,
    statut_tabac        TEXT,

    FOREIGN KEY (id_patient) REFERENCES dim_patient(id_patient)
);
CREATE INDEX IF NOT EXISTS idx_dim_suivi_patient_date ON dim_suivi_patient(id_patient, date_suivi);

CREATE TABLE IF NOT EXISTS bridge_patient_comorbidite (
    id_patient          INTEGER NOT NULL,
    id_comorbidite      INTEGER NOT NULL,
    date_diagnostic     TEXT,
    PRIMARY KEY (id_patient, id_comorbidite),
    FOREIGN KEY (id_patient)     REFERENCES dim_patient(id_patient),
    FOREIGN KEY (id_comorbidite) REFERENCES dim_comorbidite(id_comorbidite)
);

CREATE TABLE IF NOT EXISTS faits_nuits (
    id_fait_nuit        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_nuit             INTEGER NOT NULL UNIQUE,
    id_patient          INTEGER NOT NULL,
    id_temps            INTEGER NOT NULL,

    -- Indicateurs cliniques (copie depuis resultat_nuit)
    iah                 REAL,
    severite_iah        TEXT,
    spo2_min            REAL,
    spo2_moy            REAL,
    spo2_mediane        REAL,
    nb_apnees           INTEGER,
    nb_hypopnees        INTEGER,
    nb_rera             INTEGER,
    nb_microeveils      INTEGER,
    duree_sommeil_min   INTEGER,
    duree_hypoxie_min   REAL,
    position_dominante  TEXT,
    decibels_max        REAL,
    decibels_moy        REAL,
    nb_ronflements_forts INTEGER,

    -- Contexte patient au moment de cette nuit : FK vers le DERNIER
    -- suivi connu à la date de la nuit (pas de dénormalisation en
    -- dur -- dim_suivi_patient est une dimension partagée, réutilisée
    -- aussi par faits_suivi_cpap_jour)
    id_suivi_le_plus_proche  INTEGER,

    -- Caractéristiques utiles au modèle BPCO simulé
    pct_apnees_centrales REAL,   -- % d'apnées centrales parmi les apnées

    FOREIGN KEY (id_nuit)    REFERENCES dim_nuit(id_nuit),
    FOREIGN KEY (id_patient) REFERENCES dim_patient(id_patient),
    FOREIGN KEY (id_temps)   REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_suivi_le_plus_proche) REFERENCES dim_suivi_patient(id_suivi)
);
CREATE INDEX IF NOT EXISTS idx_faits_nuits_patient ON faits_nuits(id_patient);
CREATE INDEX IF NOT EXISTS idx_faits_nuits_temps    ON faits_nuits(id_temps);

CREATE TABLE IF NOT EXISTS faits_evenements (
    id_fait_evenement   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_evenement_source INTEGER NOT NULL,    -- id_evenement d'origine dans clinique_v2 (traçabilité)
    id_nuit             INTEGER NOT NULL,
    id_temps            INTEGER NOT NULL,

    type_evenement      TEXT NOT NULL,
    debut_sec           INTEGER NOT NULL,
    fin_sec             INTEGER NOT NULL,
    duree_sec           INTEGER NOT NULL,
    severite            TEXT,
    decibels            REAL,
    spo2_avant          REAL,
    spo2_apres          REAL,

    FOREIGN KEY (id_nuit)  REFERENCES dim_nuit(id_nuit),
    FOREIGN KEY (id_temps) REFERENCES dim_temps(id_temps)
);
CREATE INDEX IF NOT EXISTS idx_faits_evenements_nuit ON faits_evenements(id_nuit);
CREATE INDEX IF NOT EXISTS idx_faits_evenements_type ON faits_evenements(type_evenement);

CREATE TABLE IF NOT EXISTS faits_suivi_cpap_jour (
    id_fait_suivi_jour   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_suivi_source      INTEGER NOT NULL,   -- id_suivi d'origine dans clinique_v2 (traçabilité)
    id_patient           INTEGER NOT NULL,
    id_temps             INTEGER NOT NULL,

    duree_utilisation_h  REAL,
    iah_residuel         REAL,
    fuites_l_min         REAL,
    nb_evenements        INTEGER,
    qualite_donnee       TEXT,

    -- Contexte patient : FK vers le dernier suivi connu à cette date
    -- (même dimension partagée que faits_nuits -- permet de croiser
    -- ex: dérive de l'IAH résiduel avec l'évolution du poids)
    id_suivi_le_plus_proche INTEGER,

    -- Alertes calculées au moment de l'ETL2 (seuils cliniques standards)
    alerte_observance_insuffisante INTEGER NOT NULL DEFAULT 0,  -- 1 si duree < 4h
    alerte_iah_eleve                INTEGER NOT NULL DEFAULT 0,  -- 1 si iah_residuel > 5

    FOREIGN KEY (id_patient) REFERENCES dim_patient(id_patient),
    FOREIGN KEY (id_temps)   REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_suivi_le_plus_proche) REFERENCES dim_suivi_patient(id_suivi)
);
CREATE INDEX IF NOT EXISTS idx_faits_suivi_patient ON faits_suivi_cpap_jour(id_patient, id_temps);
CREATE INDEX IF NOT EXISTS idx_faits_suivi_alerte   ON faits_suivi_cpap_jour(alerte_observance_insuffisante, alerte_iah_eleve);

CREATE TABLE IF NOT EXISTS faits_bilan_cpap_mois (
    id_fait_bilan_mois    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_bilan_source       INTEGER NOT NULL,  -- id_bilan d'origine dans clinique_v2 (traçabilité)
    id_patient            INTEGER NOT NULL,
    annee                 INTEGER NOT NULL,
    mois                  INTEGER NOT NULL,

    duree_moy_h           REAL,
    compliance_pct        REAL,
    iah_residuel_moy      REAL,
    fuites_moy            REAL,
    nb_jours_utilises     INTEGER,
    nb_jours_non_utilises INTEGER,

    FOREIGN KEY (id_patient) REFERENCES dim_patient(id_patient),
    UNIQUE (id_patient, annee, mois)
);
CREATE INDEX IF NOT EXISTS idx_faits_bilan_patient ON faits_bilan_cpap_mois(id_patient, annee, mois);

CREATE TABLE IF NOT EXISTS etl_log_execution (
    id_execution           INTEGER PRIMARY KEY AUTOINCREMENT,
    date_execution         TEXT NOT NULL,
    nb_nuits_traitees      INTEGER DEFAULT 0,
    nb_evenements_traites  INTEGER DEFAULT 0,
    nb_suivis_cpap_traites INTEGER DEFAULT 0,
    nb_bilans_traites      INTEGER DEFAULT 0,
    statut                 TEXT DEFAULT 'succès'
);
