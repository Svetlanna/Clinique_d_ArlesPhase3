import pandas as pd


def calculer_indicateurs(df_capteur, df_events, nbapnees, nbhypopnees, nbrera, nbr_events):
    duree_reel = float((df_capteur['timestamp_sec'].max() - df_capteur['timestamp_sec'].min()) / 360)
    nb_apnees = int(nbapnees[0]) if nbapnees else 0
    nb_hypopnees = int(nbhypopnees[0]) if nbhypopnees else 0


    df_valide = df_capteur[df_capteur['spo2'] > 0]

    duree_sec = df_valide['timestamp_sec'].max() - df_valide['timestamp_sec'].min()
    duree_heures = duree_sec / 360

    stats = {

        "duree_reel": duree_reel,
        "spo2_min": float(df_capteur['spo2'].min()),
        "spo2_moy": float(df_capteur['spo2'].mean()),
        "spo2_mediane": float(df_capteur['spo2'].median()),
        "decibels_max": float(df_capteur['ronflements_db'].max()),
        "decibels_moy": float(df_capteur['ronflements_db'].mean()),
        "nbronflementsforts": int((df_capteur['ronflements_db'] > 70).sum()),
        "position_dominante": str(df_capteur['position'].mode()[0]) if not df_capteur[
            'position'].mode().empty else "Inconnue",
        "dureehypoxiemin": float((df_capteur['spo2'] < 90).sum() * (10 / 60)),

        # Extraction des valeurs des tuples et conversion en int
        "nb_apnees": int(nbapnees[0]) if nbapnees else 0,
        "nb_hypopnees": int(nbhypopnees[0]) if nbhypopnees else 0,
        "nb_rera": int(nbrera[0]) if nbrera else 0,
        "nb_microeveils": int(nbr_events[0]) if nbr_events else 0,
        "IAH": float((nb_apnees + nb_hypopnees) / duree_reel) if duree_reel > 0 else 0.0
    }

    return stats