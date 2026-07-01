import os
import re
import sys
import sqlite3
import mysql.connector  # Nécessaire pour update_nuit_in_db (mode "update")
from dotenv import load_dotenv

# Charger le .env AVANT tout le reste
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, ".env"))

# NOTE : les imports de etl.extract / etl.transform / etl.load sont volontairement
# faits en LAZY IMPORT (à l'intérieur de run_pipeline / au bloc "aucun argument"),
# et non en haut de ce fichier. Ces modules dépendent de pandas et matplotlib,
# qui ne sont nécessaires QUE pour le pipeline complet (extraction/transformation
# des données capteur), pas pour une simple mise à jour de commentaire/médecin
# (mode "update"). Ça évite de faire planter le mode "update" si pandas ou
# matplotlib ne sont pas installés dans l'environnement Python utilisé par
# l'API Node (spawn), qui n'en a normalement pas besoin.

def update_nuit_in_db(id_nuit, commentaire, id_medecin):
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        cursor = conn.cursor()

        # CORRECTION ICI : Utilisez 'notes_techniques' comme nom de colonne
        query = "UPDATE nuit_etude SET notes_techniques = %s, id_medecin = %s WHERE id_nuit = %s"

        cursor.execute(query, (commentaire, id_medecin, id_nuit))
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()

        if rows_affected == 0:
            print(f"Attention : aucune ligne mise à jour (id_nuit={id_nuit} introuvable ?)", file=sys.stderr)
            sys.exit(1)
        print("Mise à jour effectuée avec succès")
    except mysql.connector.Error as err:
        print(f"Erreur de connexion MySQL : {err}", file=sys.stderr)
        raise err

def get_ids_nuit_disponibles():
    dossier_traite = os.path.join(base_dir, "raw", "traite")
    ids = []
    if not os.path.exists(dossier_traite):
        return []
    for nom in sorted(os.listdir(dossier_traite)):
        match = re.search(r"nuit-(\d+)\.csv$", nom)
        if match:
            ids.append(int(match.group(1)))
    return ids


def run_pipeline(id_nuit):
    # Imports différés : uniquement nécessaires ici (pipeline complet)
    from etl.extract import recuperer_donnees
    from etl.transform import calculer_indicateurs
    from etl.load import (
        sauvegarder_resultats, charger_raw_capteur, copier_csv_vers_traite
    )

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
    # Point d'entrée unique
    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "update":
            # Arguments attendus: python index.py update commentaire id_medecin id
            if len(sys.argv) >= 5:
                update_nuit_in_db(int(sys.argv[4]), sys.argv[2], int(sys.argv[3]))
            else:
                print("Arguments insuffisants pour update", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                run_pipeline(int(mode))
            except ValueError:
                print("Mode inconnu ou ID de nuit invalide.", file=sys.stderr)
                sys.exit(1)
    else:
        # Aucun argument : exécute le pipeline complet
        from etl.load import creer_tables_datalake
        creer_tables_datalake()
        ids_disponibles = get_ids_nuit_disponibles()
        for id_nuit in ids_disponibles:
            run_pipeline(id_nuit)