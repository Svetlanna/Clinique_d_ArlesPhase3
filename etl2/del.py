import sqlite3
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chemin_db = os.path.join(base_dir, "etl2","base_analytique.db")
conn = sqlite3.connect(chemin_db)
cur = conn.cursor()

cur.execute("""
    DELETE FROM faits_suivi_cpap_jour WHERE id_patient = 1;
""")

conn.commit()