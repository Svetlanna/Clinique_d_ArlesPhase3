from extract2 import extract_donnees, init_db, id_patient, myconn
import pandas as pd

conn = init_db()
cur = conn.cursor()
df = extract_donnees()


conn.close()
myconn.close()

def transform_check_donnees():
    observance_heure = 4.0
    IAH_residuel_seuil = 5.0

    for _, rows in df.iterrows():
        alerte_observance_insuffisante = 1 if (rows['duree_utilisation_heures'] < observance_heure) else  0
        alerte_iah_elevee = 1 if (rows['iah_residuel'] > IAH_residuel_seuil) else  0


        duree_utilisation = rows['duree_utilisation_heures']
        iah_residuel = rows['iah_residuel']
        fuite_l_min = rows['fuite_l_min']
        nb_evenements = rows['nb_evenements']
        qualite_donnee = rows['qualite_donnee']


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
        
        id_temps = check_dim_temps()

        def cehck_id_suivi():
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
        id_suivi_le_plus_proche = cehck_id_suivi()

        cur_mysql = myconn.cursor(buffered=True)

        cur_mysql.execute("Select id_suivi from suivi_patient where id_patient = %s", (id_patient,))
        #il faut faire une autre fonction pour voir si l'id_suivi existe sur MYSQL mais comme la bdd n'est pas a jour avec le projet surtout que le front n'est pas encore fini je laisse tomber pour maintenant
        result = cur_mysql.fetchone()
        if result is None:
            raise ValueError(f"no suivi pour {id_patient}")
        id_suivi_source = result[0]


        return alerte_observance_insuffisante, alerte_iah_elevee, duree_utilisation, iah_residuel, fuite_l_min, nb_evenements, qualite_donnee, id_temps, id_suivi_le_plus_proche, id_suivi_source

conn.commit()