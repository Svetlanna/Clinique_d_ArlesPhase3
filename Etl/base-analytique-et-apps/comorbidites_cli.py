"""
CLI JSON pour la prédiction IA des comorbidités probables d'un patient.

Réimplémentation sans Streamlit du contenu de ia_comorbidites.py : même
principe (entraînement sur la galaxie SQLite déjà validée, prédiction sur
la nuit MySQL sélectionnée qui n'y est pas encore), mêmes features, mêmes
5 comorbidités les plus fréquentes, même pipeline (imputation médiane +
standardisation + RandomForest). Appelée par
Api/controllers/analytiqueController.js (GET /api/analytique/comorbidites).

Usage : python3 comorbidites_cli.py [--id_patient N] [--id_nuit N]
Sortie : un objet JSON unique sur stdout. Les erreurs sont écrites en JSON
sur stderr avec un code de sortie non nul.
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SQLITE_DB_PATH = BASE_DIR / "base_analytique.db"
IA_RANDOM_STATE = 42
IA_N_ESTIMATORS = 100

FEATURES = [
    "iah", "spo2_min", "spo2_moy",
    "nb_apnees", "nb_hypopnees", "duree_sommeil_min",
    "imc_initial", "fumeur_initial", "pa_tabac_initial",
]


def get_mysql_connection():
    load_dotenv()
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        port=int(os.environ.get("DB_PORT", "3306")),
        password=os.environ.get("DB_PASSWORD", "123456789"),
        database=os.environ.get("DB_NAME", "cliniquearles"),
    )


def charger_donnees_entrainement_sqlite():
    """Charge l'historique de la galaxie SQLite et retient les 5 comorbidités
    les plus fréquentes, avec une colonne binaire has_<comorbidite> par patient."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    try:
        df = pd.read_sql("""
            SELECT
                fn.id_patient,
                fn.iah, fn.spo2_min, fn.spo2_moy,
                fn.nb_apnees, fn.nb_hypopnees, fn.duree_sommeil_min,
                dp.imc_initial, dp.fumeur_initial, dp.pa_tabac_initial,
                GROUP_CONCAT(DISTINCT c.libelle) AS comorbidites
            FROM faits_nuits fn
            JOIN dim_patient dp ON dp.id_patient = fn.id_patient
            LEFT JOIN bridge_patient_comorbidite bpc ON bpc.id_patient = dp.id_patient
            LEFT JOIN dim_comorbidite c ON c.id_comorbidite = bpc.id_comorbidite
            GROUP BY fn.id_patient
        """, conn)
    finally:
        conn.close()

    if df.empty:
        return None, []

    toutes_comorbidites = []
    for comorb_str in df["comorbidites"].dropna():
        toutes_comorbidites.extend(comorb_str.split(","))

    top_comorbidites = pd.Series(toutes_comorbidites).value_counts().head(5).index.tolist()

    for comorb in top_comorbidites:
        df[f"has_{comorb}"] = df["comorbidites"].apply(
            lambda x: 1 if isinstance(x, str) and comorb in x.split(",") else 0
        )

    return df, top_comorbidites


def charger_donnees_patient_mysql(conn, id_nuit=None, id_patient=None):
    """Charge les indicateurs de la nuit MySQL à prédire (pas encore dans la galaxie)."""
    base_query = """
        SELECT
            r.iah, r.spo2_min, r.spo2_moy,
            r.nb_apnees, r.nb_hypopnees, r.duree_sommeil_min,
            p.imc_initial, p.fumeur AS fumeur_initial,
            p.pa_tabac AS pa_tabac_initial
        FROM resultat_nuit r
        JOIN nuit_etude n ON n.id_nuit = r.id_nuit
        JOIN patient p ON p.id_patient = n.id_patient
    """
    if id_nuit:
        query = base_query + " WHERE r.id_nuit = %s LIMIT 1"
        params = [id_nuit]
    else:
        query = base_query + " WHERE p.id_patient = %s ORDER BY r.date_validation DESC LIMIT 1"
        params = [id_patient]

    df = pd.read_sql(query, conn, params=params)
    return None if df.empty else df.iloc[0]


def entrainer_tous_modeles(df, top_comorbidites):
    """Un pipeline (imputation médiane + standardisation + RandomForest) par
    comorbidité retenue, seulement si au moins 3 cas positifs existent."""
    models = {}
    for comorb in top_comorbidites:
        if df[f"has_{comorb}"].sum() < 3:
            continue
        X = df[FEATURES]
        y = df[f"has_{comorb}"]
        pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(
                n_estimators=IA_N_ESTIMATORS,
                random_state=IA_RANDOM_STATE,
                class_weight="balanced",
            )),
        ])
        pipeline.fit(X, y)
        models[comorb] = pipeline
    return models


def predire_comorbidites(models, patient_data):
    if patient_data is None or not models:
        return {}
    X_patient = pd.DataFrame([patient_data])
    for feature in FEATURES:
        if feature not in X_patient.columns:
            X_patient[feature] = None
    X_patient = X_patient[FEATURES]

    predictions = {}
    for comorb, model in models.items():
        proba = model.predict_proba(X_patient)[0][1]
        predictions[comorb] = float(proba)
    return predictions


def niveau_risque(proba):
    if proba >= 0.7:
        return "élevé"
    if proba >= 0.5:
        return "modéré"
    return "faible"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id_patient", type=int, default=None)
    parser.add_argument("--id_nuit", type=int, default=None)
    args = parser.parse_args()

    if not args.id_patient and not args.id_nuit:
        raise RuntimeError("id_patient ou id_nuit requis")

    if not SQLITE_DB_PATH.exists():
        raise RuntimeError(f"Base analytique introuvable : {SQLITE_DB_PATH}")

    df_entrainement, top_comorbidites = charger_donnees_entrainement_sqlite()
    if df_entrainement is None or not top_comorbidites:
        raise RuntimeError("Galaxie SQLite vide : impossible d'entraîner un modèle de comorbidités.")

    models = entrainer_tous_modeles(df_entrainement, top_comorbidites)
    if not models:
        raise RuntimeError("Pas assez de cas positifs par comorbidité pour entraîner un modèle fiable.")

    mysql_conn = get_mysql_connection()
    try:
        patient_data = charger_donnees_patient_mysql(mysql_conn, id_nuit=args.id_nuit, id_patient=args.id_patient)
    finally:
        mysql_conn.close()

    if patient_data is None:
        raise RuntimeError("Aucune nuit validée (resultat_nuit) trouvée pour ce patient/cette nuit.")

    predictions = predire_comorbidites(models, patient_data)
    if not predictions:
        raise RuntimeError("Prédiction impossible avec les données disponibles.")

    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    comorbidite_principale, probabilite_principale = sorted_predictions[0]

    result = {
        "comorbidite_principale": comorbidite_principale,
        "probabilite": round(probabilite_principale, 3),
        "risque": niveau_risque(probabilite_principale),
        "toutes_predictions": [
            {"comorbidite": c, "probabilite": round(p, 3), "risque": niveau_risque(p)}
            for c, p in sorted_predictions
        ],
        "nb_patients_entrainement": int(len(df_entrainement)),
        "comorbidites_couvertes": top_comorbidites,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - on relaie toute erreur en JSON pour l'API Node
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
