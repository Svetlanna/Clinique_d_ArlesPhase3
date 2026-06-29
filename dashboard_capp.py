"""
App Dashboard : Clinique du Sommeil - Base Analytique Galaxy (CORRIGÉE)
=========================================================================
Résout :
- StreamlitDuplicateElementId (ajout de keys uniques)
- SQLite thread safety (check_same_thread=False)

Lancement :
    streamlit run app_dashboard_galaxy_fixed.py

Dépendances :
     streamlit pandas sqlite3 matplotlib sklearn plotly
"""

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime
import plotly.express as px
import seaborn as sns

# ============================================================
# CONFIGURATION
# ============================================================
DB_PATH = "base_analytique.db"

def get_connection():
    """Connexion à la base SQLite Galaxy (thread-safe)."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=True)  # CORRECTION : check_same_thread=False
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# SEUILS D'ALERTE
# ============================================================
SEUILS = {
    "iah": 30,
    "spo2_min": 85,
    "duree_hypoxie_min": 60,
    "nb_ronflements_forts": 50,
    "compliance": 80,
    "iah_residuel": 5
}

# ============================================================
# FONCTIONS DE REQUÊTES
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
    conn = sqlite3.connect("base_analytique.db")

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
    conn.close()

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

# ============================================================
# FONCTIONS D'ALERTE
# ============================================================


def check_alertes_cpap(row):
    """Vérifie les alertes pour un suivi CPAP."""
    alertes = []
    if row["alerte_observance_insuffisante"]:
        alertes.append("🔴 Observance insuffisante (< 4h)")
    if row["alerte_iah_eleve"]:
        alertes.append(f"🔴 IAH résiduel élevé = {row['iah_residuel']} (> {SEUILS['iah_residuel']})")
    if row["duree_utilisation_h"] < 4:
        alertes.append(f"⚠️ Durée = {row['duree_utilisation_h']}h (< 4h)")
    return ", ".join(alertes) if alertes else "Aucun"


@st.cache_data(ttl=300)
def get_suivi_cpap_avec_alertes():
    """Récupère les suivis CPAP avec alertes."""
    df = get_suivi_cpap_jour()
    df["alertes"] = df.apply(check_alertes_cpap, axis=1)
    return df[df["alertes"] != "Aucun"]

# ============================================================
# VISUALISATIONS
# ============================================================

def plot_cpap_compliance(df):
    """Suivi de la compliance CPAP."""
    
    # 🔹 Tri chronologique (toujours une bonne pratique)
    df = df.sort_values("date_complete")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(df["date_complete"], df["duree_utilisation_h"],
            marker='o', color="blue", label="Durée (h)")

    ax.axhline(4, color="orange", linestyle="--", label="Seuil 4h")
    ax.set_title("Observance CPAP (Derniers 30 jours)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Heures d'utilisation")
    ax.legend()

    # 🔹 Rotation des dates
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # 🔹 Afficher une date sur 5
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=len(df)//5))

    st.pyplot(fig)



def plot_patient_trends(id_patient):
    """Évolution des indicateurs pour un patient."""
    df_nuits = get_faits_nuits()
    df_nuits = df_nuits[df_nuits["id_patient"] == id_patient]

    if df_nuits.empty or len(df_nuits) < 2:
        st.warning("Pas assez de données pour ce patient.")
        return
    df_nuits = df_nuits.sort_values("date_complete", ascending=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # IAH dans le temps
    ax1.plot(df_nuits["date_complete"], df_nuits["iah"], marker='o', color="red", label="IAH")
    ax1.axhline(30, color="orange", linestyle="--", label="Seuil sévère")
    ax1.set_title(f"Évolution de l'IAH - Patient {id_patient}")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("IAH")
    ax1.legend()

    # SpO₂ min dans le temps
    ax2.plot(df_nuits["date_complete"], df_nuits["spo2_min"], marker='o', color="blue", label="SpO₂ min")
    ax2.axhline(85, color="orange", linestyle="--", label="Seuil hypoxie")
    ax2.set_title(f"Évolution de la SpO₂ min - Patient {id_patient}")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("SpO₂ min (%)")
    ax2.legend()

    plt.tight_layout()
    st.pyplot(fig)
    


# ============================================================
# INTERFACE STREAMLIT 
# ============================================================
def main():
    st.set_page_config(
        page_title="Dashboard Clinique du Sommeil",
        page_icon="🌌",
        layout="wide"
    )

    st.title("🌌 Dashboard Clinique Modèle Galaxy")
    st.markdown("---")

    # Onglets
    tab_overview, tab_alertes, tab_patients, tab_cpap, tab_ia_cpap  = st.tabs([
        "Vue d'ensemble",
        "Alertes",
        "Patients",
        "Suivi CPAP",
        "Analyse IA CAPP",
    ])


    # ============================================================
    # ONGLET 1 : VUE D'ENSEMBLE
    # ============================================================
    with tab_overview:
        st.header("Vue d'ensemble (Modèle Galaxy)")

        df_nuits = get_faits_nuits()
        df_cpap_jour = get_suivi_cpap_jour()

        # -----------------------------
        # Vérification données nuits
        # -----------------------------
        if df_nuits.empty:
            st.warning("Aucune donnée trouvée dans faits_nuits.")
        else:
            # Conversion dates
            if "date_nuit" in df_nuits.columns:
                df_nuits["date_nuit"] = pd.to_datetime(df_nuits["date_nuit"], errors="coerce")

            # -----------------------------
            # MÉTRIQUES NUIT
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total nuits", len(df_nuits))
                st.metric("Patients uniques", df_nuits["id_patient"].nunique())

            with col2:
                st.metric("Nuits SAHOS sévère", (df_nuits["iah"] > 30).sum())
                st.metric("Hypoxie > 60 min", (df_nuits["duree_hypoxie_min"] > 60).sum())



            # -----------------------------
            # MÉTRIQUES CPAP
            # -----------------------------
            if not df_cpap_jour.empty:
                st.markdown("Statistiques CPAP (30 derniers jours)")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Jours enregistrés", len(df_cpap_jour))

                with col2:
                    st.metric("Durée moyenne", f"{df_cpap_jour['duree_utilisation_h'].mean():.1f} h")

                with col3:
                    st.metric("Alertes observance", df_cpap_jour["alerte_observance_insuffisante"].sum())



    # ============================================================
    # ONGLET 2 : ALERTES
    # ============================================================
    with tab_alertes:
        st.header("Alerte CPAP jour")


        df_alertes_cpap = get_suivi_cpap_avec_alertes()
        if df_alertes_cpap.empty:
            st.success("Aucune alerte CPAP détectée.")
        else:
            st.error(f"{len(df_alertes_cpap)} alertes CPAP !")

            st.dataframe(
                df_alertes_cpap[["id_patient", "nom", "prenom", "date_complete", "duree_utilisation_h", "iah_residuel", "alertes"]],
                column_config={
                    "id_patient": st.column_config.NumberColumn("ID Patient", width="small"),
                    "nom": "Nom",
                    "prenom": "Prénom",
                    "date_complete": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                    "duree_utilisation_h": st.column_config.NumberColumn("Durée (h)", format="%.1f"),
                    "iah_residuel": st.column_config.NumberColumn("IAH résiduel", format="%.1f"),
                    "alertes": st.column_config.TextColumn("Alertes", width="large")
                },
                hide_index=True
            )

    # ============================================================
    # ONGLET 3 : PATIENTS
    # ============================================================
    with tab_patients:
        st.header("Suivi des patients")

        patients = get_patients()
        if patients.empty:
            st.warning("Aucun patient trouvé.")
        else:
            # KEY UNIQUE pour ce selectbox
            selected_patient = st.selectbox(
                "Sélectionnez un patient :",
                patients["id_patient"],
                key="patient_select_patients"  
            )
      

        patient_info = patients[patients["id_patient"] == selected_patient].iloc[0]

        # Infos patient
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ID Patient", selected_patient)
            st.metric("Nom", f"{patient_info['nom']} {patient_info['prenom']}")
        with col2:
            st.metric("Âge", f"{patient_info['age']} ans")
            st.metric("Sexe", patient_info["sexe"])
        with col3:
            st.metric("IMC initial", f"{patient_info['imc_initial']} kg/m²")


        # Historique des nuits
        st.markdown("### Historique des nuits d'étude")
        nuits = get_faits_nuits()
        nuits_patient = nuits[nuits["id_patient"] == selected_patient]
        if nuits_patient.empty:
            st.info("Aucune nuit d'étude pour ce patient.")
        else:
            st.dataframe(
                nuits_patient[["id_nuit", "date_nuit", "type_etude", "iah", "spo2_min", "duree_hypoxie_min"]],
                column_config={
                    "id_nuit": st.column_config.NumberColumn("ID Nuit", width="small"),
                    "date_nuit": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                    "type_etude": "Type",
                    "iah": st.column_config.NumberColumn("IAH", format="%.1f"),
                    "spo2_min": st.column_config.NumberColumn("SpO₂ min", format="%.1f%%"),
                },
                hide_index=True
            )

            # Évolution dans le temps
            plot_patient_trends(selected_patient)

    # ============================================================
    # ONGLET 4 : SUIVI CPAP
    # ============================================================
    with tab_cpap:
        st.header("Suivi CPAP")

        patients = get_patients()
        if patients.empty:
            st.warning("Aucun patient trouvé.")
            return

        # KEY UNIQUE pour ce selectbox
        selected_patient = st.selectbox(
            "Sélectionnez un patient :",
            patients["id_patient"],
            key="patient_select_cpap"  # KEY UNIQUE (différente de tab_patients)
        )

        # Suivi quotidien
        st.markdown("###Suivi quotidien (30 derniers jours)")
        df_cpap = get_suivi_cpap_jour(selected_patient, days=30)
        if df_cpap.empty:
            st.info("Aucun suivi CPAP pour ce patient.")
        else:
            # Métriques
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Jours enregistrés", len(df_cpap))
                st.metric("Durée moyenne", f"{df_cpap['duree_utilisation_h'].mean():.1f}h")
            with col2:
                st.metric("IAH résiduel moyen", f"{df_cpap['iah_residuel'].mean():.1f}")
                st.metric("Fuites moyennes", f"{df_cpap['fuites_l_min'].mean():.1f} L/min")
            with col3:
                st.metric("Alertes observance", df_cpap["alerte_observance_insuffisante"].sum())
                st.metric("Alertes IAH élevé", df_cpap["alerte_iah_eleve"].sum())

            # Graphique d'observance
            plot_cpap_compliance(df_cpap)

            # ============================
            # Tableau des données CPAP jour
            # ============================

            # Colonnes souhaitées
            cols_cpap = [
                "date_complete",
                "duree_utilisation_h",
                "iah_residuel",
                "fuites_l_min",
                "alertes"
            ]

            # On ne garde que celles qui existent réellement
            cols_cpap = [c for c in cols_cpap if c in df_cpap.columns]

            st.dataframe(
                df_cpap[cols_cpap],
                column_config={
                    "date_complete": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                    "duree_utilisation_h": st.column_config.NumberColumn("Durée (h)", format="%.1f"),
                    "iah_residuel": st.column_config.NumberColumn("IAH résiduel", format="%.1f"),
                    "fuites_l_min": st.column_config.NumberColumn("Fuites (L/min)", format="%.1f"),
                    "alertes": st.column_config.TextColumn("Alertes", width="medium")
                },
                hide_index=True
            )


            # ============================
            # Bilan mensuel CPAP
            # ============================

            st.markdown("###Bilan mensuel")
            df_bilan = get_bilan_cpap_mois(selected_patient)

            if df_bilan.empty:
                st.info("Aucun bilan mensuel pour ce patient.")
            else:

                cols_bilan = [
                    "annee",
                    "mois",
                    "duree_moy_h",
                    "compliance_pct",
                    "iah_residuel_moy"
                ]

                cols_bilan = [c for c in cols_bilan if c in df_bilan.columns]

                st.dataframe(
                    df_bilan[cols_bilan],
                    column_config={
                        "annee": "Année",
                        "mois": "Mois",
                        "duree_moy_h": st.column_config.NumberColumn("Durée moy (h)", format="%.1f"),
                        "compliance_pct": st.column_config.NumberColumn("Compliance (%)", format="%.1f"),
                        "iah_residuel_moy": st.column_config.NumberColumn("IAH résiduel moy", format="%.1f")
                    },
                    hide_index=True
                )

    # ============================================================
    # ONGLET 5 : IA CPAP Détection des patients à risque
    # ============================================================
    with tab_ia_cpap:
        st.header("IA CPAP : Détection précoce des patients à risque")

        df_cpap = get_suivi_cpap()  # Ton suivi CPAP jour par jour

        if df_cpap.empty:
            st.warning("Aucune donnée CPAP disponible.")
            st.stop()

        # Tri par patient + date
        df_cpap = df_cpap.sort_values(["id_patient", "date_complete"])

        # Cible : alerte le lendemain
        df_cpap["alerte_future"] = df_cpap.groupby("id_patient")["alertes"].shift(-1).fillna(0)
        df_cpap["alerte_future"] = (df_cpap["alerte_future"] > 0).astype(int)

        # Features simples
        features = [
            "duree_utilisation_h",
            "iah_residuel",
            "fuites_l_min",
            "nb_evenements"
        ]
        features = [f for f in features if f in df_cpap.columns]

        X = df_cpap[features]
        y = df_cpap["alerte_future"]

        # Vérification
        if y.sum() < 3:
            st.error("Pas assez d'alertes pour entraîner un modèle fiable.")
            st.stop()

        # Split
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Modèle simple
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42
        )
        model.fit(X_train, y_train)

        # Score
        acc = model.score(X_test, y_test)
        st.metric("Accuracy du modèle", f"{acc*100:.1f}%")

        # Probabilités
        df_cpap["prob"] = model.predict_proba(X)[:, 1]

        # Seuil
        seuil = st.slider("Seuil de risque", 0.1, 0.9, 0.35)

        # Patients à risque
        df_risque = df_cpap[(df_cpap["alerte_future"] == 0) & (df_cpap["prob"] > seuil)]

        st.subheader("Patients à risque d'alerte CPAP")

        # ALERTE AUTOMATIQUE
        if len(df_risque) > 0:
            st.error(f" {len(df_risque)} patient(s) risquent une alerte CPAP dans les prochains jours.")
        else:
            st.success("Aucun patient à risque détecté.")

        # Tableau des patients à risque
        if len(df_risque) > 0:
            st.dataframe(
                df_risque[["id_patient", "date_complete", "prob"]]
                .sort_values("prob", ascending=False)
                .rename(columns={"prob": "probabilité"})
            )

        # Importance des variables
        importances = pd.DataFrame({
            "feature": features,
            "importance": model.feature_importances_
        }).sort_values("importance", ascending=False)

        st.subheader("Variables les plus prédictives")
        st.dataframe(importances)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=importances, x="importance", y="feature", ax=ax)
        st.pyplot(fig)



if __name__ == "__main__":
    main()