from extract2 import conn, cur, load_export_1
from transform2 import load_export_2


for i in range (len(load_export_1)):
    cur.execute("""
                REPLACE INTO faits_suivi_cpap_jour (
                    id_suivi_source, id_patient, id_temps, duree_utilisation_h, iah_residuel,
                    fuites_l_min, nb_evenements, qualite_donnee,
                    id_suivi_le_plus_proche, alerte_observance_insuffisante, alerte_iah_eleve
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                load_export_1[i]['id_suivi_source'],
                load_export_1[i]['id_patient'],
                load_export_1[i]['id_temps'],
                load_export_1[i]['duree_utilisation'],
                load_export_1[i]['iah_residuel'],
                load_export_1[i]['fuite_l_min'],
                load_export_1[i]['nb_evenements'],
                load_export_1[i]['qualite_donnee'],
                load_export_1[i]['id_suivi_le_plus_proche'],
                load_export_2[i]['alerte_observance_insuffisante'],
                load_export_2[i]['alerte_iah_elevee']
            ))
conn.commit()
conn.close()
