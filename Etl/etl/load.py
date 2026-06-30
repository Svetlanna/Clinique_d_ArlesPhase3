import sqlite3
import os
import matplotlib.pyplot as plt
import shutil
import mysql.connector
import sys
from etl.extract import recuperer_donnees


def update_nuit_in_db(id_nuit, commentaire, id_medecin):
    # Charger les variables d'environnement si nécessaire
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    cursor = conn.cursor()
    query = "UPDATE nuit_etude SET notes_techniques = %s, id_medecin = %s WHERE id_nuit = %s"
    cursor.execute(query, (commentaire, id_medecin, id_nuit))
    conn.commit()
    conn.close()
    print("Mise à jour effectuée avec succès")

# Point d'entrée pour le script appelé par Node.js
if __name__ == "__main__":
    # sys.argv[0] est le script, les suivants sont les arguments
    if len(sys.argv) == 4:
        id_nuit = sys.argv[3]
        commentaire = sys.argv[1]
        id_medecin = sys.argv[2]
        update_nuit_in_db(id_nuit, commentaire, id_medecin)


def creer_tables_datalake():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'datalake.db')





    conn = sqlite3.connect(db_path)


    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_capteur (
        id_raw              INTEGER PRIMARY KEY AUTOINCREMENT,
        id_nuit             INTEGER NOT NULL,
        timestamp_sec       INTEGER NOT NULL,
        spo2                REAL,
        debitnasalpct       REAL,
        effortthoraciquepct REAL,
        position            TEXT,
        ronflements_db      REAL,
        flagevenement       INTEGER CHECK (flagevenement IN (0,1))
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS curated_nuit (
        id_curated        INTEGER PRIMARY KEY AUTOINCREMENT,
        id_nuit           INTEGER NOT NULL,
        spo2_min          REAL,
        spo2_moy          REAL,
        spo2_mediane      REAL,
        nb_apnees         INTEGER,
        nb_hypopnees      INTEGER,
        nb_rera           INTEGER,
        nb_microeveils    INTEGER,
        dureehypoxiemin   REAL,
        position_dominante TEXT,
        decibels_max      REAL,
        decibels_moy      REAL,
        nbronflementsforts INTEGER
    );
    """)

    conn.commit()
    conn.close()


def charger_raw_capteur(df_capteur, id_nuit):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'datalake.db')
    conn = sqlite3.connect(db_path)


    cursor = conn.cursor()
    cursor.execute("DELETE FROM raw_capteur WHERE id_nuit = ?", (id_nuit,))
    rows = [
        (
            id_nuit,
            int(row['timestamp_sec']),
            row.get('spo2'),
            row.get('debitnasalpct'),
            row.get('effortthoraciquepct'),
            row.get('position'),
            row.get('ronflements_db'),
            int(row['flag_evenement']) if row.get('flag_evenement') is not None else None,
        )
        for _, row in df_capteur.iterrows()
    ]

    cursor.executemany("""
    INSERT INTO raw_capteur (id_nuit, timestamp_sec, spo2, debitnasalpct, effortthoraciquepct, position, ronflements_db, flagevenement)
    VALUES (?,?,?,?,?,?,?,?)
    """, rows)

    conn.commit()
    print(f"(load.py) {len(rows)} lignes insérées dans raw_capteur pour la nuit {id_nuit}")
    conn.close()


def copier_csv_vers_traite(id_nuit):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nom_fichier = f"signal-psg-patient-{id_nuit}-nuit-{id_nuit}.csv"

    # Le fichier source est à la racine de 'raw'
    src = os.path.join(base_dir, "raw", nom_fichier)
    # Le dossier de destination est 'raw/traite'
    dst_dir = os.path.join(base_dir, "raw", "traite")

    os.makedirs(dst_dir, exist_ok=True)

    # On déplace le fichier au lieu de le copier pour éviter les doublons
    if os.path.exists(src):
        dst_path = os.path.join(dst_dir, nom_fichier)
        shutil.move(src, dst_path)
        print(f"(load.py) CSV nuit {id_nuit} déplacé vers {dst_dir}")
    else:
        print(f"(load.py) Le fichier {src} n'existe pas, il a peut-être déjà été traité.")


def sauvegarder_resultats(indicateurs, id_nuit, df_capteur):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'datalake.db')

    # Dossier dédié pour les graphiques et rapports
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM curated_nuit WHERE id_nuit = ?", (id_nuit,))

    query = """
    INSERT INTO curated_nuit (
        id_nuit, spo2_min, spo2_moy, spo2_mediane, nb_apnees, 
        nb_hypopnees, nb_rera, nb_microeveils, dureehypoxiemin, 
        position_dominante, decibels_max, decibels_moy, nbronflementsforts
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data = (
        id_nuit,
        indicateurs.get("spo2_min", 0.0),
        indicateurs.get("spo2_moy", 0.0),
        indicateurs.get("spo2_mediane", 0.0),
        indicateurs.get("nb_apnees", 0),
        indicateurs.get("nb_hypopnees", 0),
        indicateurs.get("nb_rera", 0),
        indicateurs.get("nb_microeveils", 0),
        indicateurs.get("dureehypoxiemin", 0.0),
        indicateurs.get("position_dominante", "Inconnue"),
        indicateurs.get("decibels_max", 0.0),
        indicateurs.get("decibels_moy", 0.0),
        indicateurs.get("nbronflementsforts", 0)
    )

    cursor.execute(query, data)
    conn.commit()
    UserRole="Medecine"
    if UserRole == "Medecine":

        courbSpo2 = os.path.join(output_dir, f"courbe_spo2_nuit_{id_nuit}.png")
        plt.figure()
        plt.plot(df_capteur.index, df_capteur['spo2'], marker='o')
        plt.xlabel("Temps")
        plt.ylabel("SpO2")
        plt.title(f"Évolution SpO2 - Nuit {id_nuit}")
        plt.grid(True)
        plt.savefig(courbSpo2)
        plt.close()
        print(f"Courbe SpO2 sauvegardée : {courbSpo2}")

        courbNAsal = os.path.join(output_dir, f"courbe_debit_nasal_nuit_{id_nuit}.png")
        plt.figure()
        plt.plot(df_capteur.index, df_capteur['debit_nasal_pct'], color='green')
        plt.xlabel("Temps")
        plt.ylabel("Débit Nasal")
        plt.title(f"Évolution Débit Nasal - Nuit {id_nuit}")
        plt.grid(True)
        plt.savefig(courbNAsal)
        plt.close()
        print(f"Courbe Débit Nasal sauvegardée : {courbNAsal}")

        courbRonflements = os.path.join(output_dir, f"ronflements{id_nuit}_vs_temps.png")
        plt.figure()
        plt.plot(df_capteur["timestamp_sec"], df_capteur["ronflements_db"], color="#9467bd", linewidth=1)
        plt.xlabel("Temps")
        plt.ylabel("Ronflements (dB)")
        plt.title(f"Ronflements - Nuit {id_nuit}")
        plt.grid(True)
        plt.savefig(courbRonflements)
        plt.close()
        print(f"Courbe ronflements sauvegardée : {courbRonflements}")

    cursor.execute("SELECT COUNT(*) FROM curated_nuit WHERE id_nuit = ?", (id_nuit,))
    count = cursor.fetchone()[0]
    print(f"(load.py) DEBUG: {count} ligne(s) trouvée(s) pour la nuit {id_nuit} dans {db_path}")
    rapport_path = os.path.join(output_dir, f"rapport_medecin_nuit_{id_nuit}.txt")

    with open(rapport_path, "w") as f:
        f.write(f"RAPPORT MEDECIN - Nuit {id_nuit}\n")
        f.write(f"Evolution SPO2/min: {indicateurs.get('spo2_min', 0.0)}\n")
        f.write(f"SPO2 Moyen : {indicateurs.get('spo2_moy', 0.0)}\n")
        f.write(f"SPO2 Median : {indicateurs.get('spo2_mediane', 0.0)}\n")
        f.write(f"Duree hypoxie : {indicateurs.get('dureehypoxiemin', 0.0)}\n")
        f.write(f"Position dominante : {indicateurs.get('position_dominante', 'Inconnue')}\n")
        f.write(f"Decibels Max : {indicateurs.get('decibels_max', 0.0)}\n")
        f.write(f"Decibels Moy : {indicateurs.get('decibels_moy', 0.0)}\n")
        f.write(f"nombre ronflements : {indicateurs.get('nbronflementsforts', 0)}\n")
        f.write(f"Nombre RERA : {indicateurs.get('nb_rera', 0)}\n")
        f.write(f"Nombre apnee : {indicateurs.get('nb_apnees', 0)}\n")
        # J'ai ajouté un espace avant l'accolade pour la lisibilité
        f.write(f"Nombre hypopnee : {indicateurs.get('nb_hypopnees', 0)}\n")
    print(f"Rapport écrit : {rapport_path}")






    conn.close()