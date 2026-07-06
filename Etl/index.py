import os
import re
from dotenv import load_dotenv
import sqlite3
import os
from dotenv import load_dotenv

# Charger le .env dès le départ, avant les imports locaux
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, ".env"))

# Ensuite, importez vos modules
from etl.extract import recuperer_donnees


from etl.transform import calculer_indicateurs
from etl.load import creer_tables_datalake, sauvegarder_resultats, charger_raw_capteur, copier_csv_vers_traite

def get_ids_nuit_disponibles():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    load_dotenv(dotenv_path=os.path.join(base_dir, ".env"))
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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "datalake.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Sélection de la table curated_nuit
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='curated_nuit'")
    if not cursor.fetchone():
        conn.close()
        return set()
    # Choppe les ids des nuits déja traités
    cursor.execute("SELECT DISTINCT id_nuit FROM curated_nuit")
    ids = {row[0] for row in cursor.fetchall()}
    conn.close()
    return ids


def run_pipeline(id_nuit):
    queries_response: dict = recuperer_donnees(id_nuit)
    df_capteur = queries_response['df_capteur']
    print(f"Étape 1 : Extraction :\n    {len(df_capteur)} lignes lues dans le CSV.\n    {queries_response['nbr_events'][0]} événements dans la base MySQL.")

    print("Étape 2 : Calcul des indicateurs...")
    indicateurs = calculer_indicateurs(
        queries_response['df_capteur'],
        queries_response['df_events'],
        queries_response['nbapnees'],
        queries_response['nbhypopnees'],
        queries_response['nbrera'],
        queries_response['nbr_events']
    )

    print("Étape 3 : Sauvegarde dans le Datalake...")
    charger_raw_capteur(df_capteur, id_nuit)
    sauvegarder_resultats(indicateurs, id_nuit, df_capteur)

    print("Étape 4 : Archivage du CSV brut...")
    copier_csv_vers_traite(id_nuit)

creer_tables_datalake()

ids_disponibles = get_ids_nuit_disponibles()
ids_traites = get_ids_nuit_deja_traites()

print(f"Nuits disponibles : {ids_disponibles}")
print(f"Nuits déjà dans le datalake : {sorted(ids_traites)}\n")

# run la pipeline pour chaque nuit disponible
for id_nuit in ids_disponibles:

    print(f"--- Pipeline nuit {id_nuit} ---")
    run_pipeline(id_nuit)
    print()

print("Pipeline terminé.")