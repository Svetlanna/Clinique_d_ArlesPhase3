import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os
import mysql.connector
import re



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
        alerte_iah_elevee INTEGER NOT NULL,
        UNIQUE(id_patient, id_temps)
        )
    """)
    conn.commit()
    return conn

load_dotenv()
myconn = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    port=int(os.environ.get("DB_PORT", "3306")),
    password=os.environ.get("DB_PASSWORD", "123456789"),
    database=os.environ.get("DB_NAME", "cliniquearles")
)

conn = init_db()
cur = conn.cursor()

cur.execute("""
    DELETE FROM faits_suivi_cpap_jour WHERE id_patient = 1;
""")
def extract_id(filename : str) -> tuple[int,int]:
    match = re.search(r'signal-cpap-patient-(\d+)-appareil-(\d+)\.csv', filename)
    if not match:
        raise ValueError
    else:
        return int(match.group(1)), int(match.group(2))
filename = "signal-cpap-patient-1-appareil-1.csv"
id_patient, id_appareil = extract_id(filename)



def extract_donnees(id_patient : int, id_appareil : int):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_csv = os.path.join(base_dir, "etl2", "raw_cpap", f"signal-cpap-patient-{id_patient}-appareil-{id_appareil}.csv")
    df = pd.read_csv(chemin_csv, parse_dates=["date"])
    
    load_export_1 = [] 
    for _, rows in df.iterrows():
        def check_dim_temps():
            date_str = rows["date"].strftime("%Y-%m-%d")
            cur.execute("""Select id_temps from dim_temps where date_complete = ?""", (date_str,))
            id_temps_result = cur.fetchone()
            if id_temps_result:
                return id_temps_result[0]
            else:
                date_complete = rows['date']
                
            id_temps = int(date_complete.strftime("%y%m%d"))
            annee = int(date_complete.year)
            mois = int(date_complete.month)
            jour = int(date_complete.day)
            def get_trimestre():
                trimestre = (mois - 1) // 3 + 1
                return trimestre
                    
            def jour_semaine_fr():
                jours_list = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
                jour_semaine = jours_list[date_complete.weekday()]
                return jour_semaine
                    
            def weekend():
                est_weekend = date_complete.weekday() >= 5
                return est_weekend
                    

            trimestre = get_trimestre()
            jour_semaine = jour_semaine_fr()
            est_weekend = weekend()
            cur.execute("""
                            Insert into dim_temps (id_temps, date_complete, annee, mois, jour, trimestre, jour_semaine, est_weekend)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                id_temps,
                                date_str,
                                annee,
                                mois,
                                jour,
                                trimestre,
                                jour_semaine,
                                est_weekend
                                ))
            return id_temps
            
        

            
        def check_id_suivi():
            df["date"] = pd.to_datetime(df["date"])
            target_date = rows["date"]
            idx = (df["date"] - target_date).abs().idxmin()
            nearest_date = df.loc[idx, "date"]

            cur.execute("Select id_suivi from dim_suivi_patient where id_patient = ? AND date_suivi = ? " , (id_patient, nearest_date.strftime("%Y-%m-%d")))
            id_suivi_result = cur.fetchone()
            if id_suivi_result:
                return id_suivi_result
            else: 
                return 0
        #il y a potentiellement besoin de remplir la table dim_suivi_patient mais c'est trop long (FLEMME) 
        

        cur_mysql = myconn.cursor(buffered=True)
        
        cur_mysql.execute("Select id_suivi from suivi_patient where id_patient = %s", (id_patient,))
        #il faut faire une autre fonction pour voir si l'id_suivi existe sur MYSQL mais comme la bdd n'est pas a jour avec le projet surtout que le front n'est pas encore fini je laisse tomber pour maintenant
        result = cur_mysql.fetchone()
        if result is None:
            raise ValueError(f"no suivi pour {id_patient}")
        
        id_temps = check_dim_temps()
        id_suivi_le_plus_proche = check_id_suivi()
        id_suivi_source = result[0]
        duree_utilisation = rows['duree_utilisation_heures']
        iah_residuel = rows['iah_residuel']
        fuite_l_min = rows['fuite_l_min']
        nb_evenements = rows['nb_evenements']
        qualite_donnee = rows['qualite_donnee']

        
        load_export_1.append({
        'id_patient' : id_patient,
        'id_temps': id_temps,
        'id_suivi_le_plus_proche': id_suivi_le_plus_proche,  # Fixed key name
        'id_suivi_source': id_suivi_source,  # Fixed key name
        'duree_utilisation': duree_utilisation,
        'iah_residuel': iah_residuel,
        'fuite_l_min': fuite_l_min,
        'nb_evenements': nb_evenements,
        'qualite_donnee': qualite_donnee
        })
    return df, load_export_1

df , load_export_1 = extract_donnees(id_patient, id_appareil)