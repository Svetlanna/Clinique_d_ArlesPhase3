import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

# ============================================================
# CONFIGURATION (extraction)
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH = BASE_DIR / "base_analytique.db"

def get_connection():
    """Connexion à la base SQLite Galaxy (thread-safe)."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)  # CORRECTION : check_same_thread=False
    conn.row_factory = sqlite3.Row
    return conn

conn = get_connection()

# ============================================================
# FONCTIONS DE REQUÊTES(extraction)
# ============================================================
@st.cache_data(ttl=300)  # Cache les résultats (pas la connexion)
def get_faits_nuits():
    """Récupère toutes les nuits (faits_nuits + dimensions)."""
    with get_connection() as conn:
        query = """
            SELECT
                f.*,
                p.nom, p.prenom, p.date_naissance, p.sexe, p.imc_initial,
                CAST(strftime('%Y', 'now') - strftime('%Y', p.date_naissance) -
                    (strftime('%m-%d', 'now') < strftime('%m-%d', p.date_naissance)) AS INTEGER) AS age,
                n.date_nuit, n.type_etude, n.nom_medecin,
                t.date_complete,
                s.poids, s.imc, s.tension_systolique, s.tension_diastolique
            FROM faits_nuits f
            JOIN dim_patient p ON f.id_patient = p.id_patient
            JOIN dim_nuit n ON f.id_nuit = n.id_nuit
            JOIN dim_temps t ON f.id_temps = t.id_temps
            LEFT JOIN dim_suivi_patient s ON f.id_suivi_le_plus_proche = s.id_suivi
            ORDER BY t.date_complete DESC
        """
        return pd.read_sql(query, conn)

@st.cache_data(ttl=300)
def get_patients():
    """Liste des patients (dim_patient)."""
    with get_connection() as conn:
        return pd.read_sql("""
            SELECT
                *,
                CAST(strftime('%Y', 'now') - strftime('%Y', date_naissance) -
                    (strftime('%m-%d', 'now') < strftime('%m-%d', date_naissance)) AS INTEGER) AS age
            FROM dim_patient
            ORDER BY nom, prenom
        """, conn)

@st.cache_data(ttl=300)
def get_nuit_details(id_nuit):
    """Détails d'une nuit + événements associés."""
    with get_connection() as conn:
        # Infos nuit
        nuit_query = """
            SELECT
                f.*,
                p.nom, p.prenom, p.date_naissance, p.sexe, p.imc_initial,
                CAST(strftime('%Y', 'now') - strftime('%Y', p.date_naissance) -
                    (strftime('%m-%d', 'now') < strftime('%m-%d', p.date_naissance)) AS INTEGER) AS age,
                n.date_nuit, n.type_etude, n.nom_medecin,
                t.date_complete,
                s.poids, s.imc, s.tension_systolique, s.tension_diastolique
            FROM faits_nuits f
            JOIN dim_patient p ON f.id_patient = p.id_patient
            JOIN dim_nuit n ON f.id_nuit = n.id_nuit
            JOIN dim_temps t ON f.id_temps = t.id_temps
            LEFT JOIN dim_suivi_patient s ON f.id_suivi_le_plus_proche = s.id_suivi
            WHERE f.id_nuit = ?
        """
        nuit_df = pd.read_sql(nuit_query, conn, params=[id_nuit])

        # Événements associés
        events_query = "SELECT * FROM faits_evenements WHERE id_nuit = ? ORDER BY debut_sec"
        events_df = pd.read_sql(events_query, conn, params=[id_nuit])

        return nuit_df.iloc[0] if not nuit_df.empty else None, events_df

        

def get_suivi_cpap():
    """
    Retourne le suivi CPAP jour par jour, enrichi avec la date et une colonne 'alertes'.
    """

    query = """
    SELECT
        f.id_patient,
        t.date_complete,
        f.duree_utilisation_h,
        f.iah_residuel,
        f.fuites_l_min,
        f.nb_evenements,
        f.qualite_donnee,
        f.alerte_observance_insuffisante,
        f.alerte_iah_eleve
    FROM faits_suivi_cpap_jour f
    LEFT JOIN dim_temps t ON f.id_temps = t.id_temps
    ORDER BY f.id_patient, t.date_complete;
    """

    df = pd.read_sql_query(query, conn)
    

    # Colonne synthétique d'alerte
    df["alertes"] = (
        (df["alerte_observance_insuffisante"] == 1) |
        (df["alerte_iah_eleve"] == 1)
    ).astype(int)

    return df

@st.cache_data(ttl=300)
def get_suivi_cpap_jour(id_patient=None, days=30):
    """Suivi CPAP quotidien (faits_suivi_cpap_jour)."""
    with get_connection() as conn:
        query = """
            SELECT
                f.*,
                p.nom, p.prenom, p.date_naissance,
                CAST(strftime('%Y', 'now') - strftime('%Y', p.date_naissance) -
                    (strftime('%m-%d', 'now') < strftime('%m-%d', p.date_naissance)) AS INTEGER) AS age,
                t.date_complete,
                s.poids, s.imc
            FROM faits_suivi_cpap_jour f
            JOIN dim_patient p ON f.id_patient = p.id_patient
            JOIN dim_temps t ON f.id_temps = t.id_temps
            LEFT JOIN dim_suivi_patient s ON f.id_suivi_le_plus_proche = s.id_suivi
        """
        params = []
        if id_patient:
            query += " WHERE f.id_patient = ?"
            params.append(id_patient)
        query += " ORDER BY t.date_complete DESC LIMIT ?"
        params.append(days)
        return pd.read_sql(query, conn, params=params)

@st.cache_data(ttl=300)
def get_bilan_cpap_mois(id_patient=None):
    """Bilan CPAP mensuel (faits_bilan_cpap_mois)."""
    with get_connection() as conn:
        query = """
            SELECT
                f.*,
                p.nom, p.prenom
            FROM faits_bilan_cpap_mois f
            JOIN dim_patient p ON f.id_patient = p.id_patient
        """
        params = []
        if id_patient:
            query += " WHERE f.id_patient = ?"
            params.append(id_patient)
        query += " ORDER BY f.annee DESC, f.mois DESC"
        return pd.read_sql(query, conn, params=params)

@st.cache_data(ttl=300)
def get_comorbidites_patient(id_patient):
    """Comorbidités d'un patient (bridge_patient_comorbidite)."""
    with get_connection() as conn:
        return pd.read_sql("""
            SELECT c.libelle, c.categorie, b.date_diagnostic
            FROM bridge_patient_comorbidite b
            JOIN dim_comorbidite c ON b.id_comorbidite = c.id_comorbidite
            WHERE b.id_patient = ?
            ORDER BY c.categorie, c.libelle
        """, conn, params=[id_patient])
