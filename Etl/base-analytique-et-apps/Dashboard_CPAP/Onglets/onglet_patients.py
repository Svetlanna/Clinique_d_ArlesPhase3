import streamlit as st
from dashboard_cpap_e import get_faits_nuits, get_patients
from plots import plot_patient_trends

def show_patients():
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