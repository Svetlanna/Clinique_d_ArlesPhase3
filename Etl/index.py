import os
import re
import sys
import sqlite3
from dotenv import load_dotenv

# Charger le .env
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, ".env"))

# Importez vos modules
from etl.extract import recuperer_donnees
from etl.transform import calculer_indicateurs
from etl.load import (
    creer_tables_datalake, sauvegarder_resultats,
    charger_raw_capteur, copier_csv_vers_traite, update_nuit_in_db
)


def get_ids_nuit_disponibles():
    dossier_traite = os.path.join(base_dir, "raw", "traite")
    ids = []
    if not os.path.exists(dossier_traite):
        print(f"Dossier {dossier_traite} introuvable.")
        return []
    for nom in sorted(os.listdir(dossier_traite)):
        match = re.search(r"nuit-(\d+)\.csv$", nom)
        if match:
            ids.append(int(match.group(1)))
    return ids


def get_ids_nuit_deja_traites():
    db_path = os.path.join(base_dir, "datalake.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='curated_nuit'")
    if not cursor.fetchone():
        conn.close()
        return set()
    cursor.execute("SELECT DISTINCT id_nuit FROM curated_nuit")
    ids = {row[0] for row in cursor.fetchall()}
    conn.close()
    return ids


def run_pipeline(id_nuit):
    print(f"--- Pipeline nuit {id_nuit} ---")
    queries_response = recuperer_donnees(id_nuit)
    df_capteur = queries_response['df_capteur']

    indicateurs = calculer_indicateurs(
        df_capteur,
        queries_response['df_events'],
        queries_response['nbapnees'],
        queries_response['nbhypopnees'],
        queries_response['nbrera'],
        queries_response['nbr_events']
    )

    charger_raw_capteur(df_capteur, id_nuit)
    sauvegarder_resultats(indicateurs, id_nuit, df_capteur)
    copier_csv_vers_traite(id_nuit)
    print(f"Pipeline nuit {id_nuit} terminé.")


if __name__ == "__main__":
    creer_tables_datalake()


    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "update":
            # Usage: python index.py update <commentaire> <id_medecin> <id_nuit>
            try:
                update_nuit_in_db(sys.argv[4], sys.argv[2], sys.argv[3])
            except Exception as e:
                print(f"Erreur update : {e}")
        else:

            run_pipeline(int(mode))
    else:

        ids_disponibles = get_ids_nuit_disponibles()
        for id_nuit in ids_disponibles:
            run_pipeline(id_nuit)