from extract2 import init_db
from transform2 import transform_check_donnees


conn = init_db()
cur = conn.cursor()

id_suivi_source = transform_check_donnees()
id_patient = transform_check_donnees()
id_temps = transform_check_donnees()
id_suivi_le_plus_proche = transform_check_donnees()
alerte_observance_insuffisante = transform_check_donnees()
alerte_iah_elevee = transform_check_donnees()
duree_utilisation_heures = transform_check_donnees()
iah_residuel = transform_check_donnees()
fuite_l_min = transform_check_donnees()
nb_evenements = transform_check_donnees()
qualite_donnee = transform_check_donnees()

cur.execute("""
            INSERT INTO faits_suivi_cpap_jour (
                id_suivi_source, id_patient, id_temps, duree_utilisation_h, iah_residuel,
                fuites_l_min, nb_evenements, qualite_donnee,
                id_suivi_le_plus_proche, alerte_observance_insuffisante, alerte_iah_eleve
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_suivi_source,
            id_patient,
            id_temps,
            duree_utilisation_heures,
            iah_residuel,
            fuite_l_min,
            nb_evenements,
            qualite_donnee,
            id_suivi_le_plus_proche,
            alerte_observance_insuffisante,
            alerte_iah_elevee
        ))