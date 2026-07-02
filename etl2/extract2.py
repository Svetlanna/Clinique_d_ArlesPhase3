import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os
import mysql.connector
import re

load_dotenv()
myconn = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    port=int(os.environ.get("DB_PORT", "3306")),
    password=os.environ.get("DB_PASSWORD", "123456789"),
    database=os.environ.get("DB_NAME", "cliniquearles")
)

def extract_id(filename : str) -> tuple[int,int]:
    match = re.search(r'signal-cpap-patient-(\d+)-appareil-(\d+)\.csv', filename)
    if not match:
        raise ValueError
    else:
        return int(match.group(1)), int(match.group(2))
filename = "signal-cpap-patient-1-appareil-1.csv"
id_patient, id_appareil = extract_id(filename)

def extract_donnees(id_patient : int, id_appareil : int):
   #====================================================================
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_csv = os.path.join(base_dir, "etl2", "raw_cpap", f"signal-cpap-patient-{id_patient}-appareil-{id_appareil}.csv")
    df = pd.read_csv(chemin_csv, parse_dates=["date"])
    return df
    

def init_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_db = os.path.join(base_dir, "etl2","base_analytique.db")
    conn = sqlite3.connect(chemin_db)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS faits_suivi_cpap_jour (
        id_fait_suivi_jour INTEGER PRIMARY KEY AUTOINCREMENT,
        id_suivi_source INTEGER NOT NULL,
        id_patient INTEGER NOT NULL,
        id_temps INTEGER NOT NULL,
        duree_utilisation_heures REAL NOT NULL,
        iah_residuel REAL NOT NULL,
        fuite_l_min REAL,
        nb_evenements INTEGER NOT NULL,
        qualite_donnee text NOT NULL,
        id_suivi_le_plus_proche INTEGER NOT NULL,
        alerte_observance_insuffisante INTEGER NOT NULL,
        alerte_iah_elevee INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn


extract_donnees(id_patient, id_appareil)