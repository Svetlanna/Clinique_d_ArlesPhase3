# TODO — Phase 3 : Clinique du Sommeil d'Arles

Audit initial réalisé le 02/07/2026 par comparaison entre le code du dépôt et [BRIEF.md](BRIEF.md). Mis à jour le 03/07/2026 après vérification point par point du code réel (branche `tempdev`) : dépendances Python installées, base analytique repeuplée, apps Streamlit testées et débuggées, routing Front et contrôleurs Api relus en détail.
Légende : 🔴 bloquant pour la validation du dossier · 🟠 important · 🔵 bonus / pour aller plus loin.

## 1. 🔴 Application Opérateur — branchement partiel, doublons à nettoyer

- [x] Une route + lien sidebar existent bien — mais via un **second** composant, [nuits-patients](Front/src/app/nuits-patients/nuits-patients.ts) (pluriel, routé sur `/nuitspatients`), pas le [nuits-patient](Front/src/app/nuits-patient/nuits-patient.ts) (singulier) visé initialement. Ce dernier est un doublon mort, non routé — à supprimer.
- [ ] [test-operateur.html](Front/src/app/test-operateur/test-operateur.html) est toujours 100% statique (tableau codé en dur) **et toujours routé/linké** dans la sidebar, en parallèle de Nuits Patients qui fait le vrai travail — redondance à trancher (fusionner ou retirer test-operateur du routing).
- [ ] Interface encore incomplète dans `nuits-patients.html` : le commentaire par nuit est bien éditable et sauvegardé (bouton "Enregistrer"), le `<select>` médecin est affiché — mais il ne fait office que d'affichage, aucun filtrage ni assignation n'y est branché. Le bouton "Déclencher ETL1" n'existe pas.
- [ ] Le formulaire utilise en réalité `PATCH /api/nuit/:id/commentaire` (fonctionnel, via `updateCommentaire`), pas `PUT /api/nuit/:id/update` comme prévu à l'origine. Cette dernière route existe toujours dans [nuitController.js](Api/controllers/nuitController.js) et fait un `spawn()` vers `Etl/index.py` — **ce fichier n'existe pas dans le dépôt**, la route plante donc si elle est un jour appelée.
- [x] `PYTHON_PATH` est documenté (`Api/.env.example` + section Installation du [README](README.md) racine).
- [ ] Nettoyer `nuitController.js` : `assignMedecin` est défini mais **n'est relié à aucune route** ([nuitRoutes.js](Api/routes/nuitRoutes.js) ne l'importe même pas) — code mort. `updateCommentaire` est le seul chemin réellement utilisé par le Front. `updateNuit` (avec spawn) est un chemin mort tant que `Etl/index.py` n'existe pas — supprimer ces deux morceaux ou décider explicitement de les réimplémenter.

## 2. 🔴 Application Résultats Nuit — Etl fonctionnel, Front Angular toujours un mock

- [x] Les ressources citées dans le brief sont récupérées et fonctionnelles : `app_resultats_nuit_avec_ia.py`, `ia_comorbidites.py`, le dashboard CPAP (éclaté en plusieurs fichiers dans `Dashboard_CPAP/`), les 5 modèles de prédiction de comorbidités entraînés (`models/*.pkl`). `Etl/requirements.txt` créé pour installer proprement l'environnement.
- [x] Bug corrigé : `app_resultats_nuit_avec_ia.py` fermait la connexion MySQL partagée après le premier chargement (`myconn.close()`), cassant le chargement du détail d'une nuit ("MySQL Connection not available") — les deux `.close()` en trop ont été retirés.
- [ ] [resultats-nuit.ts](Front/src/app/resultats-nuit/resultats-nuit.ts) (Front Angular) est toujours 100% mock : 3 nuits codées en dur (`[1, 2, 3]`), aucun appel API. L'app Streamlit équivalente (`app_resultats_nuit_avec_ia.py`) fonctionne bien mais reste totalement indépendante du Front Angular — rien ne les relie.
- [ ] Validation du diagnostic (action médecin, changement de statut de la nuit) : toujours pas implémentée.
- [ ] Génération PDF : toujours absente, aucune dépendance PDF côté `Api/package.json` ni côté Python.
- [ ] Insertion d'une ligne dans `faits_nuits` à la validation + synchro `dim_patient`/`dim_nuit`/`dim_temps` : toujours pas implémenté. **Point découvert entre-temps** : il existe maintenant deux copies indépendantes de la base analytique SQLite (`base_analytique.db` à la racine, utilisé par les apps Streamlit de `Etl/` ; `etl2/base_analytique.db`, utilisé par `Api/models/cpapModel.js` pour la page CPAP du Front) sans synchronisation automatique — à unifier avant d'implémenter cette écriture, sinon l'insertion se fera dans une seule des deux copies.
- [ ] Rapport uniquement : expliquer l'archivage des événements respiratoires vers une table MySQL séparée — toujours à rédiger.

## 3. 🟠 Mini ETL CPAP — fonctionnel, quelques finitions

Toujours globalement fait : [etl2/extract2.py](etl2/extract2.py) lit le CSV, calcule les deux alertes (observance < 4h, IAH résiduel > 5) et insère dans `faits_suivi_cpap_jour`.

- [ ] `id_patient` / `id_appareil` toujours codés en dur (`filename = "signal-cpap-patient-1-appareil-1.csv"`, [extract2.py:56](etl2/extract2.py)) — à paramétrer (CLI ou variable).
- [x] Typo `cehck_id_suivi` → `check_id_suivi` corrigée.
- [x] Contrainte `UNIQUE(id_patient, id_temps)` bien présente sur `faits_suivi_cpap_jour` — idempotence assurée.
- [ ] (Optionnel) exposer un déclenchement de ce script depuis l'app (endpoint Express) — pas exigé par le brief.

## 4. 🟠 Schéma galaxie + `dim_suivi_patient` (livrable obligatoire)

- [x] `dim_suivi_patient` bien modélisée, avec FK vers `faits_nuits.id_suivi_le_plus_proche` et `faits_suivi_cpap_jour.id_suivi_le_plus_proche`.
- [ ] Diagramme logique demandé par le brief : toujours aucun fichier trouvé dans le dépôt (dbdiagram.io, drawio ou mermaid conviennent) montrant où `dim_suivi_patient` s'insère dans la galaxie.

## 5. 🔴 Rapport pédagogique — non commencé

Aucun rapport structuré n'existe (seul `BRIEF.md`, qui est le cahier des charges client). Livrable obligatoire noté par compétence — mais plusieurs blocages précédents sont maintenant levés (les deux applis de démo tournent réellement, ce qui débloque leur analyse).

- [ ] C1, C2 : décrire l'extraction et les requêtes SQL (rappel ETL1 + mini ETL CPAP).
- [ ] C4 : schéma complet de la galaxie + intégration de `dim_suivi_patient` (dépend du point 4).
- [ ] C5 : documenter les procédures stockées utilisées ([Api/storedprocedure.sql](Api/storedprocedure.sql)).
- [ ] C14, C15 : justifier les choix d'architecture (Angular/Express + spawn Python pour l'app Opérateur, SQLite en étoile pour l'analytique) — et mentionner les deux instances SQLite non synchronisées (point 2) comme limite connue.
- [ ] C16, C17 : lister les composants techniques réalisés.
- [ ] CT5, CT6 : synthèse des limites des deux applis de démo — débloqué, `ia_comorbidites.py` et le dashboard CPAP tournent maintenant réellement, s'appuyer dessus en plus des limites déjà listées dans `BRIEF.md` §6.
- [ ] Expliquer le choix MySQL (opérationnel) vs SQLite en étoile (analytique) (`BRIEF.md` §5 donne déjà la trame).

## 6. 🔵 Bonus / pour aller plus loin (non prioritaire)

- [x] Découper `dashboard_cpap.py` en plusieurs fichiers — déjà fait : `dashboard_cpap_e.py` (extraction), `dashboard_cpap_t.py` (transformation/alertes), `plots.py`, `dashboard_main.py`, et un fichier par onglet dans `Onglets/`.
- [ ] Réimplémenter soi-même les deux applis de démo (`ia_comorbidites.py`, dashboard CPAP) — non retenu, elles fonctionnent telles quelles.
- [ ] Ajouter un split train/test au module comorbidités.
- [ ] Rendre les seuils de risque configurables plutôt que codés en dur (`SEUILS` dans [dashboard_cpap_t.py](Etl/base-analytique-et-apps/Dashboard_CPAP/dashboard_cpap_t.py)).
- [ ] Mettre en place un réentraînement périodique des modèles + table dédiée aux prédictions.
- [ ] Synchronisation automatique MySQL → SQLite (et entre les deux copies SQLite, cf. point 2) au moment de la validation, plutôt qu'une copie manuelle.
- [ ] Remplacer les graphiques Matplotlib/Seaborn restants par du Plotly interactif (déjà utilisé partiellement, ex. `ia_comorbidites.py`).
- [ ] Export CSV/Excel des alertes et patients à contacter.

## 7. 🟠 Dépendances manquantes

- [x] `Etl/requirements.txt` créé (`python-dotenv`, `mysql-connector-python`, `pandas`, `streamlit`, `plotly`, `matplotlib`, `seaborn`, `scikit-learn`, `joblib`).
- [ ] Aucune lib de génération PDF n'est présente (`Api/package.json` n'a ni `pdfkit` ni équivalent, rien côté Python non plus) — à ajouter côté Node ou Python selon où sera implémentée la génération du point 2.
