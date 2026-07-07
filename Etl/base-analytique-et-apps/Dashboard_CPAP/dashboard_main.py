import streamlit as st
from Onglets.onglet_overview import show_overview
from Onglets.onglet_alertes import show_alertes
from Onglets.onglet_patients import show_patients
from Onglets.onglet_cpap import show_cpap
from Onglets.onglet_ia_cpap import show_ia_cpap


# ============================================================
# INTERFACE STREAMLIT (visuel)
# ============================================================
def main():
    st.set_page_config(
        page_title="Dashboard CPAP - Clinique du Sommeil",
        page_icon="🌌",
        layout="wide"
    )

    st.title("🌌 Dashboard CPAP - Modèle Galaxy")
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
        show_overview()



    # ============================================================
    # ONGLET 2 : ALERTES
    # ============================================================
    with tab_alertes:
        show_alertes()

    # ============================================================
    # ONGLET 3 : PATIENTS
    # ============================================================
    with tab_patients:
        show_patients()

    # ============================================================
    # ONGLET 4 : SUIVI CPAP
    # ============================================================
    with tab_cpap:
        show_cpap()

    # ============================================================
    # ONGLET 5 : IA CPAP Détection des patients à risque
    # ============================================================
    with tab_ia_cpap:
        show_ia_cpap()



if __name__ == "__main__":
    main()