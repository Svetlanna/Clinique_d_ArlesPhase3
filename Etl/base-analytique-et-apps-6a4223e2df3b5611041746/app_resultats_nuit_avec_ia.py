"""
Application Streamlit pour les résultats des nuits avec prédiction de comorbidités
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import mysql.connector
from datetime import datetime

# Import du module IA
from ia_comorbidites import get_comorbidite_probable, afficher_prediction_comorbidites

# ====================== CONFIG ======================
st.set_page_config(page_title="Clinique du Sommeil", layout="wide")
st.title("Résultats des Nuits d'Étude")
st.markdown("**Clinique du Sommeil d'Arles**")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "cliniquev3"
}

NUITS_DIR = Path("nuits")

# ====================== CHARGEMENT DES DONNÉES ======================
@st.cache_data
def get_resultats(id_nuit=None):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = "CALL sp_lire_resultat_nuit(%s);"
        df = pd.read_sql(query, conn, params=[id_nuit])
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erreur BDD : {e}")
        return pd.DataFrame()

@st.cache_data
def get_liste_nuits():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql("""
            SELECT n.id_nuit, p.id_patient, p.nom, p.prenom, n.date_nuit, r.iah, r.severite_iah
            FROM nuit_etude n
            JOIN patient p ON p.id_patient = n.id_patient
            JOIN resultat_nuit r ON r.id_nuit = n.id_nuit
            ORDER BY n.date_nuit DESC
        """, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erreur liste nuits : {e}")
        return pd.DataFrame()

df_liste = get_liste_nuits()

# ====================== INTERFACE ======================
if not df_liste.empty:
    search = st.text_input(" Rechercher patient", "")

    filtered = df_liste.copy()
    if search:
        filtered = filtered[
            filtered['nom'].str.contains(search, case=False, na=False) |
            filtered['prenom'].str.contains(search, case=False, na=False)
        ]

    st.subheader(f"Nuits trouvées : {len(filtered)}")

    if not filtered.empty:
        st.dataframe(filtered, use_container_width=True, hide_index=True)

        selected_id = st.selectbox(
            "Sélectionner une nuit",
            options=filtered['id_nuit'].tolist(),
            format_func=lambda x: f"Nuit {x} : {filtered[filtered['id_nuit']==x]['nom'].iloc[0]} {filtered[filtered['id_nuit']==x]['prenom'].iloc[0]}"
        )

        # Récupérer l'ID du patient pour cette nuit
        selected_patient_id = filtered[filtered['id_nuit']==selected_id]['id_patient'].iloc[0]

        # Chargement détaillé
        detail = get_resultats(selected_id)

        if not detail.empty:
            # =============================================================
            # NOUVELLE SECTION: PRÉDICTION DES COMORBIDITÉS
            # =============================================================
            st.markdown("---")
            st.header("Analyse IA: Comorbidités Probables")

            comorbidite, probabilite, toutes_predictions = get_comorbidite_probable(
                id_nuit=selected_id,
                id_patient=selected_patient_id
            )

            if comorbidite:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader("Comorbidité la plus probable")
                with col2:
                    if probabilite >= 0.7:
                        st.error(f"{probabilite*100:.1f}%")
                    elif probabilite >= 0.5:
                        st.warning(f"{probabilite*100:.1f}%")
                    else:
                        st.success(f"{probabilite*100:.1f}%")

                st.metric(
                    label="Diagnostic IA",
                    value=comorbidite,
                    delta=f"Confiance: {probabilite*100:.1f}%"
                )

                if st.button("Voir toutes les prédictions de comorbidités"):
                    id_patient=selected_patient_id
                    id_patient = int(id_patient)

                    afficher_prediction_comorbidites(id_patient)
            else:
                st.info("Pas assez de données pour la prédiction IA.")

            st.markdown("---")

            # =============================================================
            # SECTIONS EXISTANTES
            # =============================================================
            rapport_path = NUITS_DIR / str(selected_id) / "rapport.txt"
            if rapport_path.exists():
                st.subheader(" Rapport médical complet")
                st.text_area("", rapport_path.read_text(encoding="utf-8"), height=450)
            else:
                st.warning(f"Rapport non trouvé pour la nuit {selected_id}")

            st.subheader(" Courbes de la nuit")
            nuit_dir = NUITS_DIR / str(selected_id)
            col1, col2, col3 = st.columns(3)
            for col, img, title in zip([col1,col2,col3],
                                     ["spo2.png", "debit_nasal.png", "ronflements.png"],
                                     ["SpO₂", "Débit Nasal", "Ronflements"]):
                path = nuit_dir / img
                with col:
                    if path.exists():
                        col.image(str(path), caption=title, width="stretch")
                    else:
                        col.warning(f"{img} manquant")
        else:
            st.error("Impossible de charger le détail de la nuit.")
else:
    st.warning("Aucune nuit trouvée dans la base.")

st.sidebar.caption(f"Actualisé : {datetime.now().strftime('%d/%m/%Y %H:%M')}")