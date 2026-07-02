#!/usr/bin/env python3
"""
Wrapper CLI headless de dashboard_capp.py : recalcule les 5 onglets du
dashboard (vue d'ensemble, alertes, patients, suivi CPAP, IA CPAP) et
les retourne combinés dans un seul JSON, sans rendu Streamlit/matplotlib
(les graphiques deviennent des séries de données brutes).

Usage : python3 dashboard_cli.py [--id_patient ID] [--days N] [--seuil 0.35]
"""

import argparse

import pandas as pd

from analytics_core import df_records, fail, print_result, sqlite_conn

SEUILS = {
    "iah": 30,
    "spo2_min": 85,
    "duree_hypoxie_min": 60,
    "nb_ronflements_forts": 50,
    "compliance": 80,
    "iah_residuel": 5,
}


def get_faits_nuits():
    conn = sqlite_conn()
    try:
        return pd.read_sql("""
            SELECT
                f.*,
                p.nom, p.prenom, p.date_naissance, p.sexe, p.imc_initial,
                CAST(strftime('%Y', 'now') - strftime('%Y', p.date_naissance) -
                    (strftime('%m-%d', 'now') < strftime('%m-%d', p.date_naissance)) AS INTEGER) AS age,
                n.date_nuit, n.type_etude, n.nom_medecin,
                t.date_complete,
                s.poids, s.imc, s.tension_systolique, s.tension_diastolique
            FROM faits_nuits f
            JOIN dim_patient p ON f.id_patient = p.id_patient
            JOIN dim_nuit n ON f.id_nuit = n.id_nuit
            JOIN dim_temps t ON f.id_temps = t.id_temps
            LEFT JOIN dim_suivi_patient s ON f.id_suivi_le_plus_proche = s.id_suivi
            ORDER BY t.date_complete DESC
        """, conn)
    finally:
        conn.close()


def get_patients():
    conn = sqlite_conn()
    try:
        return pd.read_sql("""
            SELECT
                *,
                CAST(strftime('%Y', 'now') - strftime('%Y', date_naissance) -
                    (strftime('%m-%d', 'now') < strftime('%m-%d', date_naissance)) AS INTEGER) AS age
            FROM dim_patient
            ORDER BY nom, prenom
        """, conn)
    finally:
        conn.close()


def get_suivi_cpap():
    conn = sqlite_conn()
    try:
        df = pd.read_sql("""
            SELECT
                f.id_patient,
                t.date_complete,
                f.duree_utilisation_h,
                f.iah_residuel,
                f.fuites_l_min,
                f.nb_evenements,
                f.qualite_donnee,
                f.alerte_observance_insuffisante,
                f.alerte_iah_eleve
            FROM faits_suivi_cpap_jour f
            LEFT JOIN dim_temps t ON f.id_temps = t.id_temps
            ORDER BY f.id_patient, t.date_complete;
        """, conn)
    finally:
        conn.close()

    df["alertes"] = (
        (df["alerte_observance_insuffisante"] == 1) | (df["alerte_iah_eleve"] == 1)
    ).astype(int)
    return df


def get_suivi_cpap_jour(id_patient=None, days=30):
    conn = sqlite_conn()
    try:
        query = """
            SELECT
                f.*,
                p.nom, p.prenom, p.date_naissance,
                CAST(strftime('%Y', 'now') - strftime('%Y', p.date_naissance) -
                    (strftime('%m-%d', 'now') < strftime('%m-%d', p.date_naissance)) AS INTEGER) AS age,
                t.date_complete,
                s.poids, s.imc
            FROM faits_suivi_cpap_jour f
            JOIN dim_patient p ON f.id_patient = p.id_patient
            JOIN dim_temps t ON f.id_temps = t.id_temps
            LEFT JOIN dim_suivi_patient s ON f.id_suivi_le_plus_proche = s.id_suivi
        """
        params = []
        if id_patient:
            query += " WHERE f.id_patient = ?"
            params.append(id_patient)
        query += " ORDER BY t.date_complete DESC LIMIT ?"
        params.append(days)
        return pd.read_sql(query, conn, params=params)
    finally:
        conn.close()


def get_bilan_cpap_mois(id_patient=None):
    conn = sqlite_conn()
    try:
        query = """
            SELECT
                f.*,
                p.nom, p.prenom
            FROM faits_bilan_cpap_mois f
            JOIN dim_patient p ON f.id_patient = p.id_patient
        """
        params = []
        if id_patient:
            query += " WHERE f.id_patient = ?"
            params.append(id_patient)
        query += " ORDER BY f.annee DESC, f.mois DESC"
        return pd.read_sql(query, conn, params=params)
    finally:
        conn.close()


def check_alertes_cpap(row):
    alertes = []
    if row["alerte_observance_insuffisante"]:
        alertes.append("Observance insuffisante (< 4h)")
    if row["alerte_iah_eleve"]:
        alertes.append(f"IAH résiduel élevé = {row['iah_residuel']} (> {SEUILS['iah_residuel']})")
    if row["duree_utilisation_h"] < 4:
        alertes.append(f"Durée = {row['duree_utilisation_h']}h (< 4h)")
    return ", ".join(alertes) if alertes else "Aucun"


def build_overview(df_nuits, df_cpap_jour):
    if df_nuits.empty:
        return {"message": "Aucune donnée trouvée dans faits_nuits."}

    overview = {
        "total_nuits": len(df_nuits),
        "patients_uniques": int(df_nuits["id_patient"].nunique()),
        "nuits_sahos_severe": int((df_nuits["iah"] > 30).sum()),
        "hypoxie_superieure_60min": int((df_nuits["duree_hypoxie_min"] > 60).sum()),
    }

    if not df_cpap_jour.empty:
        overview["cpap"] = {
            "jours_enregistres": len(df_cpap_jour),
            "duree_moyenne_h": round(float(df_cpap_jour["duree_utilisation_h"].mean()), 1),
            "alertes_observance": int(df_cpap_jour["alerte_observance_insuffisante"].sum()),
        }

    return overview


def build_alertes(df_cpap_jour):
    df = df_cpap_jour.copy()
    df["alertes"] = df.apply(check_alertes_cpap, axis=1)
    df = df[df["alertes"] != "Aucun"]

    cols = ["id_patient", "nom", "prenom", "date_complete", "duree_utilisation_h", "iah_residuel", "alertes"]
    cols = [c for c in cols if c in df.columns]
    return {"total": len(df), "alertes": df_records(df[cols])}


def build_patients(id_patient):
    patients = get_patients()
    result = {"liste": df_records(patients)}

    if patients.empty or id_patient is None:
        return result

    matching = patients[patients["id_patient"] == id_patient]
    if matching.empty:
        result["error"] = f"Patient {id_patient} introuvable"
        return result

    patient_info = matching.iloc[0]
    result["patient"] = {
        "id_patient": int(patient_info["id_patient"]),
        "nom": patient_info["nom"],
        "prenom": patient_info["prenom"],
        "age": int(patient_info["age"]) if pd.notna(patient_info["age"]) else None,
        "sexe": patient_info["sexe"],
        "imc_initial": float(patient_info["imc_initial"]) if pd.notna(patient_info["imc_initial"]) else None,
    }

    nuits = get_faits_nuits()
    nuits_patient = nuits[nuits["id_patient"] == id_patient].sort_values("date_complete")
    cols = ["id_nuit", "date_nuit", "type_etude", "iah", "spo2_min", "duree_hypoxie_min"]
    cols = [c for c in cols if c in nuits_patient.columns]
    result["historique_nuits"] = df_records(nuits_patient[cols])

    if len(nuits_patient) >= 2:
        result["evolution"] = {
            "dates": nuits_patient["date_complete"].astype(str).tolist(),
            "iah": nuits_patient["iah"].tolist(),
            "spo2_min": nuits_patient["spo2_min"].tolist(),
        }

    return result


def build_cpap(id_patient, days):
    if id_patient is None:
        return {"message": "id_patient requis pour cette section"}

    df_cpap = get_suivi_cpap_jour(id_patient, days=days)
    if df_cpap.empty:
        return {"message": "Aucun suivi CPAP pour ce patient."}

    metrics = {
        "jours_enregistres": len(df_cpap),
        "duree_moyenne_h": round(float(df_cpap["duree_utilisation_h"].mean()), 1),
        "iah_residuel_moyen": round(float(df_cpap["iah_residuel"].mean()), 1),
        "fuites_moyennes_l_min": round(float(df_cpap["fuites_l_min"].mean()), 1),
        "alertes_observance": int(df_cpap["alerte_observance_insuffisante"].sum()),
        "alertes_iah_eleve": int(df_cpap["alerte_iah_eleve"].sum()),
    }

    df_sorted = df_cpap.sort_values("date_complete")
    compliance_series = {
        "dates": df_sorted["date_complete"].astype(str).tolist(),
        "duree_utilisation_h": df_sorted["duree_utilisation_h"].tolist(),
        "seuil_h": 4,
    }

    df_cpap = df_cpap.assign(alertes=df_cpap.apply(check_alertes_cpap, axis=1))
    cols_cpap = ["date_complete", "duree_utilisation_h", "iah_residuel", "fuites_l_min", "alertes"]
    cols_cpap = [c for c in cols_cpap if c in df_cpap.columns]

    df_bilan = get_bilan_cpap_mois(id_patient)
    cols_bilan = ["annee", "mois", "duree_moy_h", "compliance_pct", "iah_residuel_moy"]
    cols_bilan = [c for c in cols_bilan if c in df_bilan.columns]

    return {
        "metrics": metrics,
        "compliance_series": compliance_series,
        "suivi_jour": df_records(df_cpap[cols_cpap]),
        "bilan_mois": df_records(df_bilan[cols_bilan]),
    }


def build_ia_cpap(seuil):
    df_cpap = get_suivi_cpap()
    if df_cpap.empty:
        return {"message": "Aucune donnée CPAP disponible."}

    df_cpap = df_cpap.sort_values(["id_patient", "date_complete"])
    df_cpap["alerte_future"] = df_cpap.groupby("id_patient")["alertes"].shift(-1).fillna(0)
    df_cpap["alerte_future"] = (df_cpap["alerte_future"] > 0).astype(int)

    features = ["duree_utilisation_h", "iah_residuel", "fuites_l_min", "nb_evenements"]
    features = [f for f in features if f in df_cpap.columns]

    X = df_cpap[features]
    y = df_cpap["alerte_future"]

    if y.sum() < 3:
        return {"error": "Pas assez d'alertes pour entraîner un modèle fiable."}

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    df_cpap["prob"] = model.predict_proba(X)[:, 1]
    df_risque = df_cpap[(df_cpap["alerte_future"] == 0) & (df_cpap["prob"] > seuil)]
    df_risque = df_risque[["id_patient", "date_complete", "prob"]].sort_values("prob", ascending=False)
    df_risque = df_risque.rename(columns={"prob": "probabilite"})

    importances = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    return {
        "accuracy": round(float(accuracy), 3),
        "seuil": seuil,
        "patients_a_risque": df_records(df_risque),
        "feature_importances": df_records(importances),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id_patient", type=int, default=None)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--seuil", type=float, default=0.35)
    args = parser.parse_args()

    df_nuits = get_faits_nuits()
    df_cpap_jour = get_suivi_cpap_jour(days=args.days)

    result = {
        "overview": build_overview(df_nuits, df_cpap_jour),
        "alertes": build_alertes(df_cpap_jour),
        "patients": build_patients(args.id_patient),
        "cpap": build_cpap(args.id_patient, args.days),
        "ia_cpap": build_ia_cpap(args.seuil),
    }

    print_result(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 - on relaie toute erreur en JSON sur stderr
        fail(e)
