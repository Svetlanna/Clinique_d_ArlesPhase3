from extract2 import df




def transform_donnees():
    observance_heure = 4.0
    IAH_residuel_seuil = 5.0
    alerts = []
    for _, rows in df.iterrows():
        alerte_observance_insuffisante = 1 if (rows['duree_utilisation_heures'] < observance_heure) else  0
        alerte_iah_elevee = 1 if (rows['iah_residuel'] > IAH_residuel_seuil) else  0
        alerts.append({
                'alerte_observance_insuffisante': alerte_observance_insuffisante,
                'alerte_iah_elevee': alerte_iah_elevee
            })
    return alerts

load_export_2 = transform_donnees()