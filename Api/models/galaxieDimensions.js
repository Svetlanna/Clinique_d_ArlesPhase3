// Fonctions partagées pour synchroniser les dimensions de la galaxie SQLite
// (dim_temps notamment, utilisée à la fois par faits_nuits et faits_suivi_cpap_jour).
// Compatible avec n'importe quelle instance better-sqlite3 dont le schéma
// correspond à base_analytique.db (racine ou etl2/).

const JOURS_FR = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];

// mysql2 renvoie les colonnes DATE sous forme d'objets Date (pas de string) ;
// les CSV/SQLite renvoient des chaînes 'YYYY-MM-DD'. On normalise les deux.
export const toDateStr = (value) => (value instanceof Date ? value.toISOString() : value).slice(0, 10);

export const idTempsFromDate = (dateStr) => Number(toDateStr(dateStr).replace(/-/g, ''));

export const upsertDimTemps = (db, dateStr) => {
    const dateComplete = toDateStr(dateStr);
    const id_temps = idTempsFromDate(dateComplete);

    const exists = db.prepare('SELECT id_temps FROM dim_temps WHERE id_temps = ?').get(id_temps);
    if (exists) return id_temps;

    const date = new Date(dateComplete);
    const annee = date.getUTCFullYear();
    const mois = date.getUTCMonth() + 1;
    const jour = date.getUTCDate();
    const trimestre = Math.floor((mois - 1) / 3) + 1;
    const jsDay = date.getUTCDay(); // 0 = dimanche
    const jour_semaine = JOURS_FR[(jsDay + 6) % 7];
    const est_weekend = (jsDay === 0 || jsDay === 6) ? 1 : 0;

    db.prepare(`
        INSERT INTO dim_temps (id_temps, date_complete, annee, mois, jour, trimestre, jour_semaine, est_weekend)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(id_temps, dateComplete, annee, mois, jour, trimestre, jour_semaine, est_weekend);

    return id_temps;
};

export const upsertDimPatient = (db, patient) => {
    db.prepare(`
        INSERT INTO dim_patient (
            id_patient, nom, prenom, date_naissance, sexe,
            imc_initial, fumeur_initial, pa_tabac_initial, profession, niveau_activite, date_maj
        ) VALUES (@id_patient, @nom, @prenom, @date_naissance, @sexe,
                  @imc_initial, @fumeur_initial, @pa_tabac_initial, @profession, @niveau_activite, @date_maj)
        ON CONFLICT(id_patient) DO UPDATE SET
            nom = excluded.nom,
            prenom = excluded.prenom,
            date_naissance = excluded.date_naissance,
            sexe = excluded.sexe,
            imc_initial = excluded.imc_initial,
            fumeur_initial = excluded.fumeur_initial,
            pa_tabac_initial = excluded.pa_tabac_initial,
            profession = excluded.profession,
            niveau_activite = excluded.niveau_activite,
            date_maj = excluded.date_maj
    `).run(patient);
};

export const upsertDimNuit = (db, nuit) => {
    db.prepare(`
        INSERT INTO dim_nuit (id_nuit, date_nuit, type_etude, nom_medecin, modele_appareil_psg)
        VALUES (@id_nuit, @date_nuit, @type_etude, @nom_medecin, @modele_appareil_psg)
        ON CONFLICT(id_nuit) DO UPDATE SET
            date_nuit = excluded.date_nuit,
            type_etude = excluded.type_etude,
            nom_medecin = excluded.nom_medecin,
            modele_appareil_psg = excluded.modele_appareil_psg
    `).run(nuit);
};
