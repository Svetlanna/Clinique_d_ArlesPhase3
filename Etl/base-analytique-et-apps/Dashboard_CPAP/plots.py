import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dashboard_cpap_e import get_faits_nuits


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
    
