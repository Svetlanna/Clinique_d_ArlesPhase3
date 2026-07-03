import streamlit as st
from dashboard_cpap_e import get_suivi_cpap_jour, get_patients, get_bilan_cpap_mois
from plots import plot_cpap_compliance


def show_cpap():
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