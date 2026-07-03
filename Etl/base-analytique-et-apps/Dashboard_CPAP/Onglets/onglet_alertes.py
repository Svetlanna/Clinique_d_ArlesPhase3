import streamlit as st
from dashboard_cpap_t import get_suivi_cpap_avec_alertes


def show_alertes():
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