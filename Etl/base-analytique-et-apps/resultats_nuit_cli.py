#!/usr/bin/env python3
"""
Wrapper CLI headless de app_resultats_nuit_avec_ia.py : même logique
de requêtage (liste des nuits + détail d'une nuit + prédiction IA des
comorbidités + rapport + courbes), mais imprime du JSON au lieu de
rendre une UI Streamlit. Appelé en sous-processus par l'Api Node.

Usage : python3 resultats_nuit_cli.py [--id_nuit ID] [--search TEXTE]
"""

import argparse
import sys

import pandas as pd

from analytics_core import NUITS_DIR, df_records, fail, mysql_conn, print_result
from comorbidites_core import predire_pour


def get_liste_nuits(search=None):
    conn = mysql_conn()
    try:
        df = pd.read_sql("""
            SELECT n.id_nuit, p.id_patient, p.nom, p.prenom, n.date_nuit, r.iah, r.severite_iah
            FROM nuit_etude n
            JOIN patient p ON p.id_patient = n.id_patient
            JOIN resultat_nuit r ON r.id_nuit = n.id_nuit
            ORDER BY n.date_nuit DESC
        """, conn)
    finally:
        conn.close()

    if search:
        df = df[
            df["nom"].str.contains(search, case=False, na=False)
            | df["prenom"].str.contains(search, case=False, na=False)
        ]
    return df


def get_detail(id_nuit):
    conn = mysql_conn()
    try:
        return pd.read_sql("CALL sp_lire_resultat_nuit(%s);", conn, params=[id_nuit])
    finally:
        conn.close()


def get_courbes(nuit_dir):
    courbes = {}
    for key, filename in [
        ("spo2", "spo2.png"),
        ("debit_nasal", "debit_nasal.png"),
        ("ronflements", "ronflements.png"),
    ]:
        path = nuit_dir / filename
        courbes[key] = {"exists": path.exists(), "path": str(path) if path.exists() else None}
    return courbes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id_nuit", type=int, default=None)
    parser.add_argument("--search", type=str, default=None)
    args = parser.parse_args()

    liste = get_liste_nuits(args.search)
    result = {
        "liste_nuits": df_records(liste),
        "total": len(liste),
        "detail": None,
        "comorbidite_ia": None,
        "rapport": None,
        "courbes": None,
    }

    if args.id_nuit:
        detail = get_detail(args.id_nuit)
        if not detail.empty:
            row = detail.iloc[0]
            result["detail"] = df_records(detail)[0]

            result["comorbidite_ia"] = predire_pour(
                id_nuit=args.id_nuit, id_patient=int(row["id_patient"])
            )

            nuit_dir = NUITS_DIR / str(args.id_nuit)
            rapport_path = nuit_dir / "rapport.txt"
            result["rapport"] = (
                rapport_path.read_text(encoding="utf-8") if rapport_path.exists() else None
            )
            result["courbes"] = get_courbes(nuit_dir)

    print_result(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 - on relaie toute erreur en JSON sur stderr
        fail(e)
