"""
Application Streamlit pour les résultats des nuits avec prédiction de comorbidités
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import pymysql
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Import du module IA
from ia_comorbidites import get_comorbidite_probable, afficher_prediction_comorbidites

# ====================== CONFIG ======================
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:3000")
ANGULAR_BASE_URL = os.environ.get("ANGULAR_BASE_URL", "http://localhost:4200")

st.set_page_config(page_title="Clinique du Sommeil", layout="wide")
st.title("Résultats des Nuits d'Étude")
st.markdown("**Clinique du Sommeil d'Arles**")

load_dotenv()
myconn = pymysql.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    port=int(os.environ.get("DB_PORT", "3306")),
    password=os.environ.get("DB_PASSWORD", "123456789"),
    database=os.environ.get("DB_NAME", "cliniquearles"),
)


BASE_DIR = Path(__file__).resolve().parent.parent
NUITS_DIR = BASE_DIR / "outputs"


# ====================== CHARGEMENT DES DONNÉES ======================
@st.cache_data
def get_resultats(id_nuit=None):
    try:
        query = "CALL sp_lire_resultat_nuit(%s);"
        df = pd.read_sql(query, myconn, params=[id_nuit])
        return df
    except Exception as e:
        st.error(f"Erreur BDD : {e}")
        return pd.DataFrame()

@st.cache_data
def get_liste_nuits():
    try:
        df = pd.read_sql("""
            SELECT n.id_nuit, p.id_patient, p.nom, p.prenom, n.date_nuit, r.iah, r.severite_iah
            FROM nuit_etude n
            JOIN patient p ON p.id_patient = n.id_patient
            JOIN resultat_nuit r ON r.id_nuit = n.id_nuit
            ORDER BY n.date_nuit DESC
        """, myconn)
        return df
    except Exception as e:
        st.error(f"Erreur liste nuits : {e}")
        return pd.DataFrame()

@st.cache_data
def get_medecins():
    try:
        return pd.read_sql("""
            SELECT m.id_personnel, pm.nom, pm.prenom
            FROM medecin m
            JOIN personnel pm ON pm.id_personnel = m.id_personnel
            ORDER BY pm.nom
        """, myconn)
    except Exception as e:
        st.error(f"Erreur liste médecins : {e}")
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
        st.dataframe(filtered, width="stretch", hide_index=True)

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
            rapport_path = NUITS_DIR / f"rapport_medecin_nuit_{(selected_id)}.txt"
            if rapport_path.exists():
                st.subheader(" Rapport médical complet")
                try:
                    rapport_text = rapport_path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    rapport_text = rapport_path.read_text(encoding="cp1252")
                st.text_area("Rapport médical", rapport_text, height=450)
            else:
                st.warning(f"Rapport non trouvé pour la nuit {selected_id}")

            st.subheader(" Courbes de la nuit")
            nuit_dir = NUITS_DIR
            col1, col2, col3 = st.columns(3)
            for col, (img, title) in zip([col1,col2,col3],
                                       [
                                     (f"courbe_spo2_nuit_{selected_id}.png", "SpO₂"), 
                                     (f"courbe_debit_nasal_nuit_{selected_id}.png", "Débit Nasal"), 
                                     (f"ronflements{selected_id}_vs_temps.png", "Ronflements")
                                     ]
            ):
                path = nuit_dir / img
                with col:
                    if path.exists():
                        col.image(str(path), caption=title, width="stretch")
                    else:
                        col.warning(f"{img} manquant")

            # =============================================================
            # OPÉRATION : VALIDATION DU DIAGNOSTIC
            # Même logique que la page Angular /nuitspatients : deux actions
            # indépendantes (médecin validateur / commentaire), chacune un
            # simple PATCH sur resultat_nuit, sans recalcul des indicateurs.
            # =============================================================
            st.markdown("---")
            st.subheader("Valider le diagnostic")

            df_medecins = get_medecins()
            col_medecin, col_commentaire, col_redirect = st.columns([1, 1, 1])

            medecin_actuel = int(detail['id_medecin'].iloc[0]) if 'id_medecin' in detail.columns and pd.notna(detail['id_medecin'].iloc[0]) else None
            commentaire_actuel = detail['commentaire_medical'].iloc[0] if 'commentaire_medical' in detail.columns and pd.notna(detail['commentaire_medical'].iloc[0]) else ""

            with col_medecin:
                if df_medecins.empty:
                    st.warning("Aucun médecin trouvé.")
                else:
                    medecins_ids = df_medecins['id_personnel'].tolist()
                    medecin_id = st.selectbox(
                        "Médecin validateur",
                        options=medecins_ids,
                        index=medecins_ids.index(medecin_actuel) if medecin_actuel in medecins_ids else 0,
                        format_func=lambda x: f"Dr {df_medecins[df_medecins['id_personnel']==x]['nom'].iloc[0]} {df_medecins[df_medecins['id_personnel']==x]['prenom'].iloc[0]}",
                        key=f"medecin_validateur_{selected_id}",
                    )

                    if st.button("Enregistrer le médecin", key=f"btn_medecin_{selected_id}"):
                        try:
                            reponse = requests.patch(
                                f"{API_BASE_URL}/api/nuit/{selected_id}/medecin",
                                json={"idMedecin": int(medecin_id)},
                                timeout=15,
                            )
                            reponse.raise_for_status()
                            st.success("Médecin validateur enregistré.")
                            get_resultats.clear()
                        except requests.exceptions.RequestException as e:
                            detail_err = ""
                            if e.response is not None:
                                try:
                                    detail_err = e.response.json().get("message", "")
                                except ValueError:
                                    detail_err = e.response.text
                            st.error(f"Échec de l'enregistrement : {detail_err or e}")

            with col_commentaire:
                commentaire = st.text_area(
                    "Commentaire médical",
                    value=commentaire_actuel,
                    key=f"commentaire_{selected_id}",
                )

                if st.button("Enregistrer le commentaire", key=f"btn_commentaire_{selected_id}"):
                    try:
                        reponse = requests.patch(
                            f"{API_BASE_URL}/api/nuit/{selected_id}/commentaire",
                            json={"commentaire": commentaire},
                            timeout=15,
                        )
                        reponse.raise_for_status()
                        st.success("Commentaire enregistré.")
                        get_resultats.clear()
                    except requests.exceptions.RequestException as e:
                        detail_err = ""
                        if e.response is not None:
                            try:
                                detail_err = e.response.json().get("message", "")
                            except ValueError:
                                detail_err = e.response.text
                        st.error(f"Échec de l'enregistrement : {detail_err or e}")

            with col_redirect:
                st.link_button(
                    "Ouvrir la fiche patient dans CliniquePlus",
                    f"{ANGULAR_BASE_URL}/nuitspatients",
                )
        else:
            st.error("Impossible de charger le détail de la nuit.")
else:
    st.warning("Aucune nuit trouvée dans la base.")

st.sidebar.caption(f"Actualisé : {datetime.now().strftime('%d/%m/%Y %H:%M')}")