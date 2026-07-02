# TODO — Phase 3 : Clinique du Sommeil d'Arles

Audit réalisé le 02/07/2026 par comparaison entre le code du dépôt (branche `tempdev`) et [BRIEF.md](BRIEF.md).
Légende : 🔴 bloquant pour la validation du dossier · 🟠 important · 🔵 bonus / pour aller plus loin.

## 1. 🔴 Application Opérateur — branchement incomplet

Le backend et le composant de données existent déjà mais ne sont **pas accessibles dans l'app** : la page réellement routée est un mock.

- [ ] Ajouter la route `nuits-patient` dans [Front/src/app/app.routes.ts](Front/src/app/app.routes.ts) et le lien correspondant dans [sidebar.html](Front/src/app/components/sidebar/sidebar.html) — le composant [nuits-patient.ts](Front/src/app/nuits-patient/nuits-patient.ts) consomme déjà `GET /api/nuit` mais n'est référencé nulle part dans le routing actuel.
- [ ] [test-operateur.html](Front/src/app/test-operateur/test-operateur.html) est actuellement 100% statique (tableau d'appareils codé en dur : "ARL-0042", "Martin, J.", etc.) — soit le remplacer par la vraie page opérateur, soit le supprimer une fois `nuits-patient` intégré.
- [ ] Dans `nuits-patient.html`, ajouter les éléments d'interface manquants : sélection d'une nuit, champ commentaire, `<select>` médecin (les données sont déjà dispo via `GET /api/med`), bouton "Déclencher ETL1".
- [ ] Relier ce formulaire à `PUT /api/nuit/:id/update` ([nuitController.js:119-154](Api/controllers/nuitController.js)), qui fait déjà le `spawn()` vers `Etl/index.py` — actuellement cet endpoint n'est appelé par aucun code front.
- [ ] Afficher un retour utilisateur (loading/succès/erreur) pendant l'exécution du process Python spawné, actuellement silencieux côté front.
- [ ] Vérifier que `PYTHON_PATH` est documenté (README/`.env.example`) et tester le déclenchement de bout en bout (front → API → spawn → ETL1 → datalake).
- [ ] Nettoyer la redondance : `updateCommentaire` / `assignMedecin` (routes séparées, non utilisées) vs `updateNuit` (route combinée avec spawn) dans `nuitController.js` — clarifier laquelle est le vrai chemin utilisé.

## 2. 🔴 Application Résultats Nuit — non commencée

C'est un livrable obligatoire. Le composant front existe mais est un simple mock d'images statiques ; aucune des fonctionnalités demandées n'est implémentée.

- [ ] Récupérer les ressources manquantes citées dans le brief : `app_resultats_nuit_avec_ia.py`, `ia_comorbidites.py`, `dashboard_cpap.py`, `base_analytique_et_apps.zip`, `Random Forest en Médecine.pdf`. Le dossier [Etl/base-analytique-et-apps-6a4223e2df3b5611041746/](Etl/base-analytique-et-apps-6a4223e2df3b5611041746/) ne contient qu'un `.venv` vide, aucun de ces fichiers n'est présent dans le dépôt.
- [ ] [resultats-nuit.ts](Front/src/app/resultats-nuit/resultats-nuit.ts) affiche 3 images/rapports codés en dur (`nuit_1`, `nuit_2`, `nuit_3`) — remplacer par une vraie liste de nuits + rapport/courbes réels par nuit sélectionnée.
- [ ] Implémenter la validation du diagnostic (action médecin, changement de statut de la nuit).
- [ ] Générer le PDF complet dans le dossier du patient à la validation — aucune dépendance PDF n'est présente ni côté `Api/package.json` ni détectée côté Python (pas de `requirements.txt` dans le repo).
- [ ] À la validation, insérer une ligne dans `faits_nuits` de la galaxie ([etl2/base_analytique.db](etl2/base_analytique.db) — schéma déjà correct) et synchroniser `dim_patient`, `dim_nuit`, `dim_temps` si elles n'existent pas encore pour cette nuit.
- [ ] Rapport uniquement : expliquer pourquoi l'archivage des événements respiratoires vers une table MySQL séparée serait nécessaire à terme, et proposer le schéma de cette table (pas d'implémentation demandée).

## 3. 🟠 Mini ETL CPAP — fonctionnel, quelques finitions

Contrairement aux deux points précédents, ce livrable obligatoire est globalement fait : [etl2/extract2.py](etl2/extract2.py) lit le CSV, calcule correctement les deux alertes (observance < 4h, IAH résiduel > 5) et insère dans `faits_suivi_cpap_jour`. Le CSV de test ([etl2/raw_cpap/signal-cpap-patient-1-appareil-1.csv](etl2/raw_cpap/signal-cpap-patient-1-appareil-1.csv)) correspond bien au patient 1 = "Tessier" et couvre juin 2026 avec plusieurs jours d'alerte (double alerte les 04/06 et 06/06 notamment).

- [ ] Rendre `id_patient` / `id_appareil` paramétrables (CLI ou variable) au lieu du nom de fichier codé en dur `filename = "signal-cpap-patient-1-appareil-1.csv"` ([extract2.py:24](etl2/extract2.py)).
- [ ] Corriger le nom de fonction `cehck_id_suivi` → `check_id_suivi` (typo, [extract2.py:91](etl2/extract2.py)).
- [ ] Vérifier l'idempotence : aucune contrainte `UNIQUE(id_patient, id_temps)` visible sur `faits_suivi_cpap_jour` — relancer le script deux fois duplique probablement les lignes.
- [ ] (Optionnel) exposer un déclenchement de ce script depuis l'app (endpoint Express), le brief ne l'exige pas mais ça faciliterait la démo.

## 4. 🟠 Schéma galaxie + `dim_suivi_patient` (livrable obligatoire)

- [x] La table `dim_suivi_patient` est déjà modélisée dans `etl2/base_analytique.db`, avec FK vers `faits_nuits.id_suivi_le_plus_proche` et `faits_suivi_cpap_jour.id_suivi_le_plus_proche`.
- [ ] Produire le diagramme logique demandé par le brief (aucun fichier diagramme trouvé dans le dépôt — dbdiagram.io, drawio ou mermaid conviennent) montrant où `dim_suivi_patient` s'insère dans la galaxie et quels faits s'y rattachent.

## 5. 🔴 Rapport pédagogique — non commencé

Aucun rapport structuré n'existe (seul `BRIEF.md`, qui est le cahier des charges client, pas un livrable produit par l'équipe). C'est un livrable obligatoire noté par compétence.

- [ ] C1, C2 : décrire l'extraction et les requêtes SQL (rappel ETL1 + mini ETL CPAP).
- [ ] C4 : schéma complet de la galaxie + intégration de `dim_suivi_patient` (dépend du point 4).
- [ ] C5 : documenter les procédures stockées utilisées ([Api/storedprocedure.sql](Api/storedprocedure.sql)).
- [ ] C14, C15 : justifier les choix d'architecture (Angular/Express + spawn Python pour l'app Opérateur, SQLite en étoile pour l'analytique).
- [ ] C16, C17 : lister les composants techniques réalisés.
- [ ] CT5, CT6 : synthèse des limites des deux applis de démo (`ia_comorbidites.py`, `dashboard_cpap.py`) — bloqué tant que ces fichiers ne sont pas récupérés (voir point 2), s'appuyer en attendant sur les limites déjà listées dans `BRIEF.md` §6.
- [ ] Expliquer le choix MySQL (opérationnel) vs SQLite en étoile (analytique) (`BRIEF.md` §5 donne déjà la trame).

## 6. 🔵 Bonus / pour aller plus loin (non prioritaire)

- [ ] Réimplémenter soi-même les deux applis de démo (`ia_comorbidites.py`, `dashboard_cpap.py`).
- [ ] Ajouter un split train/test au module comorbidités.
- [ ] Rendre les seuils de risque configurables plutôt que codés en dur.
- [ ] Mettre en place un réentraînement périodique des modèles + table dédiée aux prédictions.
- [ ] Synchronisation automatique MySQL → SQLite au moment de la validation, plutôt qu'un ETL manuel.
- [ ] Remplacer Matplotlib/Seaborn par des graphiques Plotly interactifs.
- [ ] Export CSV/Excel des alertes et patients à contacter.
- [ ] Découper `dashboard_cpap.py` en plusieurs fichiers (config, requêtage, IA, interface).

## 7. 🟠 Dépendances manquantes

- [ ] Aucun `requirements.txt` n'existe pour les scripts Python (`Etl/`, `etl2/`) — en créer un (`pandas`, `mysql-connector-python`, `python-dotenv`, et `scikit-learn`/`reportlab` si les points 2 et 6 sont traités).
- [ ] Aucune lib de génération PDF n'est présente (`Api/package.json` n'a ni `pdfkit` ni équivalent) — à ajouter côté Node ou Python selon où sera implémentée la génération du point 2.
