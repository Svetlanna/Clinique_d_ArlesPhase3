"""
ia_comorbidites.py
===================
Module IA pour prédire les comorbidités probables d'un patient.

Entraîné sur la base analytique SQLite (galaxie), prédit sur les
données fraîches de MySQL (clinique_v2).

Toutes les colonnes utilisées correspondent aux vraies colonnes de
nos deux schémas :
  - resultat_nuit / faits_nuits : iah, spo2_min, spo2_moy, nb_apnees,
    nb_hypopnees, duree_sommeil_min
  - patient / dim_patient : imc_initial, fumeur_initial, pa_tabac_initial
  - dim_comorbidite : libelle (pas "nom_comorbidite")
"""

from pathlib import Path
import pandas as pd
import mysql.connector
import sqlite3
import streamlit as st
import joblib
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# =============================================================================
# CONFIGURATION
# =============================================================================

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "cliniquev3"
}

SQLITE_PATH = Path("base_analytique.db")

IA_RANDOM_STATE = 42
IA_N_ESTIMATORS = 100
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

# Les features utilisées pour entraîner et prédire -- ce sont les
# SEULES colonnes réellement disponibles dans nos deux bases.
FEATURES = [
    "iah", "spo2_min", "spo2_moy",
    "nb_apnees", "nb_hypopnees", "duree_sommeil_min",
    "imc_initial", "fumeur_initial", "pa_tabac_initial",
]


# =============================================================================
# ENTRAINEMENT (sur SQLite, la galaxie)
# =============================================================================

@st.cache_resource
def charger_donnees_entrainement_sqlite():
    """
    Charge les données d'entraînement depuis la galaxie SQLite.

    faits_nuits porte déjà id_patient directement -- pas besoin de
    repasser par dim_nuit pour retrouver le patient.
    """
    try:
        conn = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
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
        conn.close()

        if df.empty:
            return None, None

        # Liste des comorbidités présentes, on garde les 5 plus fréquentes
        toutes_comorbidites = []
        for comorb_str in df["comorbidites"].dropna():
            toutes_comorbidites.extend(comorb_str.split(","))

        top_comorbidites = (
            pd.Series(toutes_comorbidites).value_counts().head(5).index.tolist()
        )

        # Une colonne binaire par comorbidité retenue
        for comorb in top_comorbidites:
            df[f"has_{comorb}"] = df["comorbidites"].apply(
                lambda x: 1 if isinstance(x, str) and comorb in x.split(",") else 0
            )

        return df, top_comorbidites

    except Exception as e:
        st.error(f"Erreur SQLite : {e}")
        return None, None


# =============================================================================
# CHARGEMENT DES NOUVELLES DONNÉES (MySQL)
# =============================================================================

@st.cache_data(ttl=300)
def charger_nouvelle_nuit_mysql(id_nuit=None, id_patient=None):
    """
    Charge les données d'une nuit (ou la dernière nuit d'un patient)
    depuis MySQL, avec les vraies colonnes de resultat_nuit et patient.
    """
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)

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

        conn.close()

        if df.empty:
            return None

        return df.iloc[0]

    except Exception as e:
        st.error(f"Erreur MySQL : {e}")
        return None


# =============================================================================
# ENTRAINEMENT DES MODÈLES
# =============================================================================

def entrainer_modele(comorbidite, df):
    """Entraîne un pipeline simple (imputation + standardisation + RandomForest)."""
    try:
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
    except Exception as e:
        st.error(f"Erreur entraînement {comorbidite} : {e}")
        return None


@st.cache_resource
def entrainer_tous_modeles(df, top_comorbidites):
    """Entraîne un modèle par comorbidité retenue, et sauvegarde sur disque."""
    models = {}
    for comorb in top_comorbidites:
        # On n'entraîne que s'il y a au moins quelques cas positifs --
        # sinon le modèle n'a rigoureusement aucune valeur prédictive.
        if df[f"has_{comorb}"].sum() < 3:
            continue
        model = entrainer_modele(comorb, df)
        if model:
            models[comorb] = model
            joblib.dump(model, MODELS_DIR / f"modele_{comorb}.pkl")
    return models


# =============================================================================
# PRÉDICTION
# =============================================================================

def predire_comorbidites(models, patient_data):
    """Prédit la probabilité de chaque comorbidité pour un patient donné."""
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


# =============================================================================
# FONCTIONS PRINCIPALES (appelées depuis l'app Streamlit)
# =============================================================================

def _assurer_modeles_charges():
    """Entraîne les modèles une seule fois par session, les garde en cache."""
    if "comorbidite_models" not in st.session_state:
        with st.spinner("Entraînement des modèles sur la base analytique..."):
            df, top_comorbidites = charger_donnees_entrainement_sqlite()
            if df is not None and top_comorbidites:
                st.session_state["comorbidite_models"] = entrainer_tous_modeles(df, top_comorbidites)
            else:
                st.session_state["comorbidite_models"] = {}
    return st.session_state["comorbidite_models"]


def get_comorbidite_probable(id_nuit=None, id_patient=None):
    """Retourne (comorbidité la plus probable, probabilité, toutes les prédictions)."""
    models = _assurer_modeles_charges()
    if not models:
        return None, 0, {}

    patient_data = charger_nouvelle_nuit_mysql(id_nuit=id_nuit, id_patient=id_patient)
    if patient_data is None:
        return None, 0, {}

    predictions = predire_comorbidites(models, patient_data)
    if not predictions:
        return None, 0, {}

    best_comorb = max(predictions.items(), key=lambda x: x[1])
    return best_comorb[0], best_comorb[1], predictions


def afficher_prediction_comorbidites(id_patient=None):
    """Affiche l'interface complète de prédiction pour un patient."""
    st.subheader("Prédiction des comorbidités (sur données MySQL)")

    models = _assurer_modeles_charges()
    if not models:
        st.error("Base analytique vide ou pas assez de cas pour entraîner un modèle.")
        return

    if id_patient is None:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        df_patients = pd.read_sql("SELECT id_patient, nom, prenom FROM patient", conn)
        conn.close()
        id_patient = st.selectbox(
            "Sélectionner un patient",
            options=df_patients["id_patient"].tolist(),
            format_func=lambda x: f"{df_patients[df_patients['id_patient']==x]['nom'].iloc[0]} "
                                   f"{df_patients[df_patients['id_patient']==x]['prenom'].iloc[0]}",
            key="select_patient_comorb"

        )
        id_patient = int(id_patient)

    patient_data = charger_nouvelle_nuit_mysql(id_patient=id_patient)
    if patient_data is None:
        st.warning("Aucune donnée MySQL disponible pour ce patient.")
        return

    with st.spinner("Prédiction en cours..."):
        predictions = predire_comorbidites(models, patient_data)

    if not predictions:
        st.info("Pas assez de données pour la prédiction.")
        return

    st.subheader("Résultats de la prédiction")
    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

    for comorb, proba in sorted_predictions:
        if proba >= 0.7:
            color, risque = "🔴", "Élevé"
        elif proba >= 0.5:
            color, risque = "🟡", "Modéré"
        else:
            color, risque = "🟢", "Faible"

        st.metric(label=f"{color} {comorb}", value=f"{proba*100:.1f}%", delta=f"Risque : {risque}")

    fig = go.Figure(go.Bar(
        x=[p[1]*100 for p in sorted_predictions],
        y=[p[0] for p in sorted_predictions],
        orientation="h",
        marker=dict(
            color=[p[1]*100 for p in sorted_predictions],
            colorscale="RdYlGn_r",
            showscale=True,
            colorbar=dict(title="Probabilité %")
        )
    ))
    fig.update_layout(
        title="Probabilité des comorbidités",
        xaxis_title="Probabilité (%)",
        yaxis_title="Comorbidité",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)