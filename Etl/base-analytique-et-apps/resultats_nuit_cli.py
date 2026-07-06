"""
CLI JSON pour l'application Résultats Nuit (liste des nuits validées,
détail complet d'une nuit, rapport médical, chemins des courbes).

Réimplémentation sans Streamlit du contenu de app_resultats_nuit_avec_ia.py
(get_liste_nuits, get_resultats via la procédure stockée sp_lire_resultat_nuit).
Appelée par Api/controllers/analytiqueController.js
(GET /api/analytique/resultats-nuit).

Usage : python3 resultats_nuit_cli.py [--id_nuit N] [--search texte]
Sortie : un objet JSON unique sur stdout. Les erreurs sont écrites en JSON
sur stderr avec un code de sortie non nul.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import pymysql
import pandas as pd
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"


def get_mysql_connection():
    load_dotenv()
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        port=int(os.environ.get("DB_PORT", "3306")),
        password=os.environ.get("DB_PASSWORD", "123456789"),
        database=os.environ.get("DB_NAME", "cliniquearles"),
        cursorclass=pymysql.cursors.DictCursor,
    )


def df_to_records(df):
    if df.empty:
        return []
    return json.loads(df.to_json(orient="records", date_format="iso"))


def get_liste_nuits(conn, search=None):
    df = pd.read_sql("""
        SELECT n.id_nuit, p.id_patient, p.nom, p.prenom, n.date_nuit, r.iah, r.severite_iah
        FROM nuit_etude n
        JOIN patient p ON p.id_patient = n.id_patient
        JOIN resultat_nuit r ON r.id_nuit = n.id_nuit
        ORDER BY n.date_nuit DESC
    """, conn)
    if search:
        mask = (
            df["nom"].str.contains(search, case=False, na=False)
            | df["prenom"].str.contains(search, case=False, na=False)
        )
        df = df[mask]
    return df


def get_detail_nuit(conn, id_nuit):
    df = pd.read_sql("CALL sp_lire_resultat_nuit(%s);", conn, params=[id_nuit])
    return None if df.empty else df.iloc[0]


def get_rapport_et_courbes(id_nuit):
    rapport_path = OUTPUTS_DIR / f"rapport_medecin_nuit_{id_nuit}.txt"
    courbes = {
        "spo2": f"courbe_spo2_nuit_{id_nuit}.png",
        "debit_nasal": f"courbe_debit_nasal_nuit_{id_nuit}.png",
        "ronflements": f"ronflements{id_nuit}_vs_temps.png",
    }
    return {
        "rapport_texte": rapport_path.read_text(encoding="utf-8") if rapport_path.exists() else None,
        "courbes": {
            cle: {"fichier": nom, "existe": (OUTPUTS_DIR / nom).exists()}
            for cle, nom in courbes.items()
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id_nuit", type=int, default=None)
    parser.add_argument("--search", type=str, default=None)
    args = parser.parse_args()

    conn = get_mysql_connection()
    try:
        result = {"liste_nuits": df_to_records(get_liste_nuits(conn, args.search))}

        if args.id_nuit:
            detail = get_detail_nuit(conn, args.id_nuit)
            if detail is None:
                raise RuntimeError(f"Aucun résultat validé pour la nuit {args.id_nuit}.")
            detail_dict = json.loads(detail.to_json(date_format="iso"))
            detail_dict.update(get_rapport_et_courbes(args.id_nuit))
            result["detail"] = detail_dict
    finally:
        conn.close()

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - on relaie toute erreur en JSON pour l'API Node
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
