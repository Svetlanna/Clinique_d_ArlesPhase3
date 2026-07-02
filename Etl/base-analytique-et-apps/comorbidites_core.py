"""
Logique de prédiction des comorbidités, portée depuis ia_comorbidites.py
sans les appels Streamlit (st.cache_*, st.spinner, st.error). Entraîne
les modèles à la volée à chaque appel : un wrapper CLI est un processus
court qui ne vit pas assez longtemps pour bénéficier d'un cache disque.
"""

import pandas as pd

from analytics_core import mysql_conn, sqlite_conn

FEATURES = [
    "iah", "spo2_min", "spo2_moy",
    "nb_apnees", "nb_hypopnees", "duree_sommeil_min",
    "imc_initial", "fumeur_initial", "pa_tabac_initial",
]

IA_RANDOM_STATE = 42
IA_N_ESTIMATORS = 100


def charger_donnees_entrainement_sqlite():
    conn = sqlite_conn()
    try:
        query = """
            SELECT
                fn.id_patient,
                fn.iah,
                fn.spo2_min,
                fn.spo2_moy,
                fn.nb_apnees,
                fn.nb_hypopnees,
                fn.duree_sommeil_min,
                dp.imc_initial,
                dp.fumeur_initial,
                dp.pa_tabac_initial,
                GROUP_CONCAT(DISTINCT c.libelle) AS comorbidites
            FROM faits_nuits fn
            JOIN dim_patient dp ON dp.id_patient = fn.id_patient
            LEFT JOIN bridge_patient_comorbidite bpc ON bpc.id_patient = dp.id_patient
            LEFT JOIN dim_comorbidite c ON c.id_comorbidite = bpc.id_comorbidite
            GROUP BY fn.id_patient
        """
        df = pd.read_sql(query, conn)
    finally:
        conn.close()

    if df.empty:
        return None, None

    toutes_comorbidites = []
    for comorb_str in df["comorbidites"].dropna():
        toutes_comorbidites.extend(comorb_str.split(","))

    top_comorbidites = (
        pd.Series(toutes_comorbidites).value_counts().head(5).index.tolist()
    )

    for comorb in top_comorbidites:
        df[f"has_{comorb}"] = df["comorbidites"].apply(
            lambda x: 1 if isinstance(x, str) and comorb in x.split(",") else 0
        )

    return df, top_comorbidites


def charger_nouvelle_nuit_mysql(id_nuit=None, id_patient=None):
    conn = mysql_conn()
    try:
        if id_nuit:
            query = """
                SELECT
                    r.iah, r.spo2_min, r.spo2_moy,
                    r.nb_apnees, r.nb_hypopnees, r.duree_sommeil_min,
                    p.imc_initial, p.fumeur AS fumeur_initial,
                    p.pa_tabac AS pa_tabac_initial
                FROM resultat_nuit r
                JOIN nuit_etude n ON n.id_nuit = r.id_nuit
                JOIN patient p ON p.id_patient = n.id_patient
                WHERE r.id_nuit = %s
                LIMIT 1
            """
            df = pd.read_sql(query, conn, params=[id_nuit])
        else:
            query = """
                SELECT
                    r.iah, r.spo2_min, r.spo2_moy,
                    r.nb_apnees, r.nb_hypopnees, r.duree_sommeil_min,
                    p.imc_initial, p.fumeur AS fumeur_initial,
                    p.pa_tabac AS pa_tabac_initial
                FROM resultat_nuit r
                JOIN nuit_etude n ON n.id_nuit = r.id_nuit
                JOIN patient p ON p.id_patient = n.id_patient
                WHERE p.id_patient = %s
                ORDER BY r.date_validation DESC
                LIMIT 1
            """
            df = pd.read_sql(query, conn, params=[id_patient])
    finally:
        conn.close()

    if df.empty:
        return None
    return df.iloc[0]


def entrainer_modele(comorbidite, df):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    y = df[f"has_{comorbidite}"]
    X = df[FEATURES]

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=IA_N_ESTIMATORS,
            random_state=IA_RANDOM_STATE,
            class_weight="balanced"
        ))
    ])
    pipeline.fit(X, y)
    return pipeline


def entrainer_tous_modeles(df, top_comorbidites):
    models = {}
    for comorb in top_comorbidites:
        if df[f"has_{comorb}"].sum() < 3:
            continue
        models[comorb] = entrainer_modele(comorb, df)
    return models


def predire_comorbidites(models, patient_data):
    predictions = {}
    if patient_data is None or not models:
        return predictions

    X_patient = pd.DataFrame([patient_data])
    for feature in FEATURES:
        if feature not in X_patient.columns:
            X_patient[feature] = None
    X_patient = X_patient[FEATURES]

    for comorb, model in models.items():
        try:
            proba = model.predict_proba(X_patient)[0][1]
            predictions[comorb] = float(proba)
        except Exception:
            predictions[comorb] = 0.0

    return predictions


def niveau_risque(probabilite):
    if probabilite >= 0.7:
        return "eleve"
    if probabilite >= 0.5:
        return "modere"
    return "faible"


def predire_pour(id_nuit=None, id_patient=None):
    """Retourne le détail des prédictions de comorbidités, ou None si pas assez de données."""
    df, top_comorbidites = charger_donnees_entrainement_sqlite()
    if df is None or not top_comorbidites:
        return None

    models = entrainer_tous_modeles(df, top_comorbidites)
    if not models:
        return None

    patient_data = charger_nouvelle_nuit_mysql(id_nuit=id_nuit, id_patient=id_patient)
    if patient_data is None:
        return None

    predictions = predire_comorbidites(models, patient_data)
    if not predictions:
        return None

    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    return {
        "comorbidite_principale": sorted_predictions[0][0],
        "probabilite_principale": sorted_predictions[0][1],
        "predictions": [
            {"comorbidite": c, "probabilite": p, "risque": niveau_risque(p)}
            for c, p in sorted_predictions
        ],
    }
