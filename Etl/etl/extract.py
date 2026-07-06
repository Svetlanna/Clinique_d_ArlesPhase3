import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import glob

load_dotenv()

def recuperer_donnees(id_nuit : int):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_csv = os.path.join(base_dir, "raw", "traite", f"signal-psg-patient-{id_nuit}-nuit-{id_nuit}.csv")

    df_capteur = pd.read_csv(chemin_csv)

    # lecture des événements (MySQL)
    # Change the connection block in extract.py to this:
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

    cur = conn.cursor(buffered=True)
    cur.execute('SELECT * FROM evenement_respiratoire WHERE id_nuit = %s', (id_nuit,))
    df_events = cur.fetchall()

    # Des bugs apparaissent lorsque chaque query est execute séparement
    # recours a une fnction local pour fix
    def count_events(cursor, id_nuit, types=None):
        if types:
            placeholders = ", ".join(["%s"] * len(types))
            cursor.execute(
                f"SELECT COUNT(*) FROM evenement_respiratoire WHERE id_nuit = %s AND type_evenement IN ({placeholders})",
                (id_nuit, *types)
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM evenement_respiratoire WHERE id_nuit = %s",
                (id_nuit,)
            )
        return cursor.fetchone()

    nbapnees = count_events(cur, id_nuit, ["apnée obstructive", "apnée centrale"])
    nbhypopnees = count_events(cur, id_nuit, ["hypopnée"])
    nbrera = count_events(cur, id_nuit, ["RERA"])
    nbr_events = count_events(cur, id_nuit)

    queries_response = {
        'df_capteur': df_capteur,
        'df_events': df_events,
        'nbapnees': nbapnees,
        'nbhypopnees': nbhypopnees,
        'nbrera': nbrera,
        'nbr_events': nbr_events,
    }
    print(f"  apnées={nbapnees[0]}, hypopnées={nbhypopnees[0]}, RERA={nbrera[0]}, total={nbr_events[0]}")
    conn.close()

    return queries_response