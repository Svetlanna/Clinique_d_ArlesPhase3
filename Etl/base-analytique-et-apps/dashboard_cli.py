"""
CLI JSON pour le dashboard analytique (vue d'ensemble, alertes, patients,
suivi CPAP, prédiction IA du risque d'alerte du lendemain).

Réimplémentation sans dépendance à Streamlit du contenu de Dashboard_CPAP/
(dashboard_cpap_e.py, dashboard_cpap_t.py, Onglets/*.py), pour être appelée
par Api/controllers/analytiqueController.js (GET /api/analytique/dashboard).

Usage : python3 dashboard_cli.py [--id_patient N] [--days 30] [--seuil 0.35]
Sortie : un objet JSON unique sur stdout. Les erreurs sont écrites en JSON
sur stderr avec un code de sortie non nul.
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "base_analytique.db"

SEUIL_IAH_SEVERE = 30
SEUIL_HYPOXIE_MIN = 60


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def df_to_records(df):
    if df.empty:
        return []
    return json.loads(df.to_json(orient="records", date_format="iso"))


def get_faits_nuits(conn):
    return pd.read_sql("""
        SELECT f.*, p.nom, p.prenom, n.date_nuit, n.type_etude, n.nom_medecin, t.date_complete
        FROM faits_nuits f
        JOIN dim_patient p ON f.id_patient = p.id_patient
        JOIN dim_nuit n ON f.id_nuit = n.id_nuit
        JOIN dim_temps t ON f.id_temps = t.id_temps
        ORDER BY t.date_complete DESC
    """, conn)


def get_patients(conn):
    return pd.read_sql("""
        SELECT *,
            CAST(strftime('%Y', 'now') - strftime('%Y', date_naissance) -
                (strftime('%m-%d', 'now') < strftime('%m-%d', date_naissance)) AS INTEGER) AS age
        FROM dim_patient
        ORDER BY nom, prenom
    """, conn)


def get_suivi_cpap_jour(conn, id_patient=None, days=30):
    query = """
        SELECT f.*, p.nom, p.prenom, t.date_complete
        FROM faits_suivi_cpap_jour f
        JOIN dim_patient p ON f.id_patient = p.id_patient
        JOIN dim_temps t ON f.id_temps = t.id_temps
    """
    params = []
    if id_patient:
        query += " WHERE f.id_patient = ?"
        params.append(id_patient)
    query += " ORDER BY t.date_complete DESC LIMIT ?"
    params.append(days)
    return pd.read_sql(query, conn, params=params)


def get_bilan_cpap_mois(conn, id_patient=None):
    query = """
        SELECT f.*, p.nom, p.prenom
        FROM faits_bilan_cpap_mois f
        JOIN dim_patient p ON f.id_patient = p.id_patient
    """
    params = []
    if id_patient:
        query += " WHERE f.id_patient = ?"
        params.append(id_patient)
    query += " ORDER BY f.annee DESC, f.mois DESC"
    return pd.read_sql(query, conn, params=params)


def build_overview(conn):
    nuits = get_faits_nuits(conn)
    cpap = get_suivi_cpap_jour(conn, days=30)
    return {
        "total_nuits": int(len(nuits)),
        "patients_uniques": int(nuits["id_patient"].nunique()) if not nuits.empty else 0,
        "nuits_severes": int((nuits["iah"] > SEUIL_IAH_SEVERE).sum()) if not nuits.empty else 0,
        "hypoxie_superieure_60min": int((nuits["duree_hypoxie_min"] > SEUIL_HYPOXIE_MIN).sum()) if not nuits.empty else 0,
        "jours_cpap_enregistres": int(len(cpap)),
        "duree_moyenne_h": round(float(cpap["duree_utilisation_h"].mean()), 1) if not cpap.empty else None,
        "alertes_observance": int(cpap["alerte_observance_insuffisante"].sum()) if not cpap.empty else 0,
        "alertes_iah": int(cpap["alerte_iah_eleve"].sum()) if not cpap.empty else 0,
    }


def build_alertes(conn):
    cpap = get_suivi_cpap_jour(conn, days=100000)
    if cpap.empty:
        return []

    def libelle_alertes(row):
        alertes = []
        if row["alerte_observance_insuffisante"]:
            alertes.append("Observance insuffisante (< 4h)")
        if row["alerte_iah_eleve"]:
            alertes.append(f"IAH résiduel élevé ({row['iah_residuel']})")
        return ", ".join(alertes)

    cpap["alertes"] = cpap.apply(libelle_alertes, axis=1)
    alertes = cpap[cpap["alertes"] != ""]
    cols = ["id_patient", "nom", "prenom", "date_complete", "duree_utilisation_h", "iah_residuel", "alertes"]
    return df_to_records(alertes[cols])


def build_ia_cpap(conn, seuil):
    cpap = get_suivi_cpap_jour(conn, days=100000)
    if cpap.empty:
        return {"error": "Aucune donnée CPAP disponible."}

    cpap = cpap.sort_values(["id_patient", "date_complete"])
    cpap["alerte"] = ((cpap["alerte_observance_insuffisante"] == 1) | (cpap["alerte_iah_eleve"] == 1)).astype(int)
    cpap["alerte_future"] = cpap.groupby("id_patient")["alerte"].shift(-1).fillna(0)
    cpap["alerte_future"] = (cpap["alerte_future"] > 0).astype(int)

    features = [f for f in ["duree_utilisation_h", "iah_residuel", "fuites_l_min", "nb_evenements"] if f in cpap.columns]
    X = cpap[features].fillna(0)
    y = cpap["alerte_future"]

    if y.sum() < 3:
        return {"error": "Pas assez d'alertes pour entraîner un modèle fiable (minimum 3 requis)."}

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    accuracy = float(model.score(X_test, y_test))

    cpap["prob"] = model.predict_proba(X)[:, 1]
    risques = cpap[(cpap["alerte_future"] == 0) & (cpap["prob"] > seuil)].sort_values("prob", ascending=False)

    importances = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    return {
        "accuracy": round(accuracy, 3),
        "seuil": seuil,
        "patients_a_risque": df_to_records(
            risques[["id_patient", "date_complete", "prob"]].rename(columns={"prob": "probabilite"})
        ),
        "importances": df_to_records(importances),
    }


def build_patient_detail(conn, id_patient, days):
    patients = get_patients(conn)
    info = patients[patients["id_patient"] == id_patient]
    if info.empty:
        return {"error": f"Patient {id_patient} introuvable dans la galaxie."}

    nuits = get_faits_nuits(conn)
    nuits_patient = nuits[nuits["id_patient"] == id_patient]
    cpap = get_suivi_cpap_jour(conn, id_patient=id_patient, days=days)
    bilan = get_bilan_cpap_mois(conn, id_patient=id_patient)
    comorbidites = pd.read_sql("""
        SELECT c.libelle, c.categorie, b.date_diagnostic
        FROM bridge_patient_comorbidite b
        JOIN dim_comorbidite c ON b.id_comorbidite = c.id_comorbidite
        WHERE b.id_patient = ?
        ORDER BY c.categorie, c.libelle
    """, conn, params=[id_patient])

    return {
        "info": df_to_records(info)[0],
        "historique_nuits": df_to_records(
            nuits_patient[["id_nuit", "date_nuit", "type_etude", "iah", "severite_iah", "spo2_min", "duree_hypoxie_min"]]
        ),
        "suivi_cpap": df_to_records(
            cpap[["date_complete", "duree_utilisation_h", "iah_residuel", "fuites_l_min",
                  "alerte_observance_insuffisante", "alerte_iah_eleve"]]
        ),
        "bilan_mensuel": df_to_records(
            bilan[["annee", "mois", "duree_moy_h", "compliance_pct", "iah_residuel_moy"]]
        ),
        "comorbidites": df_to_records(comorbidites),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id_patient", type=int, default=None)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--seuil", type=float, default=0.35)
    args = parser.parse_args()

    if not DB_PATH.exists():
        raise RuntimeError(f"Base analytique introuvable : {DB_PATH}")

    conn = get_connection()
    try:
        result = {
            "overview": build_overview(conn),
            "alertes": build_alertes(conn),
            "patients": df_to_records(get_patients(conn)[["id_patient", "nom", "prenom", "age", "sexe", "imc_initial"]]),
            "ia_cpap": build_ia_cpap(conn, args.seuil),
        }
        if args.id_patient:
            result["patient_detail"] = build_patient_detail(conn, args.id_patient, args.days)
        print(json.dumps(result, ensure_ascii=False))
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - on relaie toute erreur en JSON pour l'API Node
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
