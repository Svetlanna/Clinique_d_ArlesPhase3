#!/usr/bin/env python3
"""
Wrapper CLI headless de ia_comorbidites.py : prédiction autonome des
comorbidités probables pour un patient ou une nuit, en JSON.

Usage : python3 comorbidites_cli.py (--id_patient ID | --id_nuit ID)
"""

import argparse

from analytics_core import fail, print_result
from comorbidites_core import predire_pour


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id_patient", type=int, default=None)
    parser.add_argument("--id_nuit", type=int, default=None)
    args = parser.parse_args()

    if not args.id_patient and not args.id_nuit:
        raise ValueError("id_patient ou id_nuit requis")

    result = predire_pour(id_nuit=args.id_nuit, id_patient=args.id_patient)
    if result is None:
        result = {
            "comorbidite_principale": None,
            "probabilite_principale": 0,
            "predictions": [],
            "message": "Pas assez de données pour la prédiction IA.",
        }

    print_result(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 - on relaie toute erreur en JSON sur stderr
        fail(e)
