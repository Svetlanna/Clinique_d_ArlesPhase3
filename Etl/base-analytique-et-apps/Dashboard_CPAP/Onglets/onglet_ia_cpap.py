import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from dashboard_cpap_e import get_suivi_cpap


def show_ia_cpap():
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