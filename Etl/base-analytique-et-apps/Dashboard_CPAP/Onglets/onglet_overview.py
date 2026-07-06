import streamlit as st
from dashboard_cpap_e import get_faits_nuits, get_suivi_cpap_jour
import pandas as pd

def show_overview():
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