import streamlit as st
from dashboard_cpap_e import get_suivi_cpap_jour

# ============================================================
# SEUILS D'ALERTE (transformation)
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
# FONCTIONS D'ALERTE (transformation)
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
