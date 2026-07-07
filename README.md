# Clinique Plus - Application Opérateur/Médecin

[![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://www.javascript.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Angular](https://img.shields.io/badge/Angular-E23237?style=for-the-badge&logo=angular&logoColor=white)](https://angular.io/)
[![Express](https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white)](https://expressjs.com/)
[![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AI](https://img.shields.io/badge/AI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=for-the-badge&logo=sass&logoColor=white)](https://sass-lang.com/)
[![Trello](https://img.shields.io/badge/Trello-0052CC?style=for-the-badge&logo=trello&logoColor=white)](https://trello.com/)

Ce projet consiste en un prototype de DPI complet intégrant des briques IA pour assurer la supervision des nuits d'études au sein de la clinique du sommeil d'Arles (fictif) : détection/validation des événements respiratoires d'une nuit et prédiction des comorbidités probables d'un patient (`Etl/base-analytique-et-apps/ia_comorbidites.py`, un RandomForest par comorbidité).

## Utilisation

| N° étape | Description | Illustration |
| --- | --- | --- |
| 1 | L'utilisateur est initialement rendu sur une page de connexion lui demandant d'indiquer ses identifiants de connexions | | 
| 2 | Un tableau de bord d'accueil est affiché à l'utilisateur mentionnant quelques informations général sur la clinique et son profil | |
| 3 | L'utilisateur peut se rendre aux pages accessible pour son rôle | |

## UML / Diagramme d'utilisation

![image](schemas_et_diagramme/diagram_projet.drawio.png)

## Diagramme base de données :

### 1. Base MySQL

![image](schemas_et_diagramme/mld_mysql/schema_bdd_leger.jpg)

### 2. Datalake

![image](schemas_et_diagramme/mld_datalake/schema_bdd_datalake.jpg) 

### 3. Base analytique

![image](schemas_et_diagramme/mld_base_analytique/schema_bdd_analytique.jpg)

# Installation
### 1. Initialiser les bases de données
Ce projet dipose de deux bases de données :
- Une base MySQL opérationnelle (`cliniquearles`), utilisée par l'Api Express.
- Un datalake SQLite analytique en modèle galaxie/constellation, utilisé par les apps Streamlit du dossier `Etl/` et par le mini ETL CPAP de l'Api (`POST /api/analytique/cpap/import`, via `Api/models/cpapModel.js`).

**Base MySQL** : dans un schéma vierge nommé `cliniquearles`, exécutez dans l'ordre :
1. [Api/dbmigration.sql](Api/dbmigration.sql) — schéma + données de démo (dump le plus à jour, à privilégier sur `clinique2nuitsv2.sql` qui est une version antérieure du même dump).
2. [Api/storedprocedure.sql](Api/storedprocedure.sql) — procédures stockées utilisées par l'Api (`sp_compteur_*`).

`Api/auth_migration.sql` existe (colonnes `password_hash`, tables `user_role`/`refresh_token`) mais n'est **pas branché au code actuel** : `authController.js` compare encore le mot de passe en clair via la table `utilisateur`. Inutile de le jouer sauf si vous reprenez le chantier d'authentification hashée (le script `seed.js` qu'il mentionne n'existe pas non plus dans le dépôt).

**Datalake SQLite** : les fichiers `.db` sont ignorés par git (`.gitignore`), donc absents d'un clone fraîchement cloné. Il n'y a pas de script qui reconstruit le schéma complet de la galaxie depuis zéro dans ce dépôt (seul `etl2/extract2.py` sait créer/alimenter la table `faits_suivi_cpap_jour`) — récupérez un `base_analytique.db` pré-rempli auprès de l'équipe et placez-le à deux endroits :
- `base_analytique.db` à la racine (lu par les apps Streamlit de `Etl/`)
- `etl2/base_analytique.db` (alimenté par `Api/models/cpapModel.js` lors du mini ETL CPAP)

Ce sont deux copies indépendantes du même fichier, sans synchronisation automatique : si vous relancez `etl2/extract2.py`, pensez à recopier le fichier mis à jour vers la racine pour que les apps Streamlit voient les nouvelles données.

**Modèles IA (comorbidités)** : `models/` à la racine contient un `.pkl` par comorbidité (RandomForest entraîné via `Etl/base-analytique-et-apps/ia_comorbidites.py`, features = indicateurs de nuit + IMC/tabac du patient). Le dossier est créé/rempli automatiquement au premier lancement de l'app Streamlit "Résultats nuit (IA)" si absent — aucune étape manuelle requise.

### 2. Installez les dépendences :
Afin que le projet soit fonctionnel, les environnements comprenant les dépendences nécessaires au fonctionnement du projet doivent être installés.

> il est supposé que vous disposiez déja de NPM, node, nodemon et python localement. 

Positionnez-vous à la racine de votre projet et effectuez ces commandes :

```bash 
cd Api
cp ../.env.example .env
npm install
```
** Veuillez renseigner les bons identifiants de connexion à votre base de données MYSQL créér précédemment (`DB_NAME=cliniquearles`), ainsi que `PYTHON_PATH` (ex. `python3` sous Linux/macOS) : l'Api lance des scripts Python (`Etl/index.py`) en sous-processus pour certaines mises à jour de nuit.
```bash
cd ../Front
npm install
```
```bash
cd ../Etl
python3 -m venv .venv
```
```bash
source .venv/bin/activate   # Windows : .venv\Scripts\activate
python3 -m pip install -r requirements.txt
```

Les scripts Python (`Etl/`, `etl2/`) chargent leurs identifiants MySQL via un second `.env`, **à la racine du projet** (différent de `Api/.env`) :
```bash
cd ..
cat > .env << 'EOF'
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_NAME=cliniquearles
EOF
```

### 3. Lancer le projet

Positionnez-vous à la racine de votre projet, et dans des terminaux séparés :

```bash
cd Api/
nodemon
```

```bash
cd Front/
ng serve
```

Les deux apps Streamlit du dossier `Etl/` (base analytique déjà initialisée requise, cf. étape 1) sont accessibles depuis des liens de la sidebar Angular (`Front/src/app/components/sidebar/`), avec des ports **codés en dur côté front** (`sidebar.ts`) : elles doivent donc impérativement tourner sur ces ports précis pour que les liens fonctionnent.

```bash
cd Etl/base-analytique-et-apps
streamlit run app_resultats_nuit_avec_ia.py --server.port 8501
```
```bash
cd Etl/base-analytique-et-apps/Dashboard_CPAP
streamlit run dashboard_main.py --server.port 8502
```

- "Résultats nuit (Validation)" (port 8501, visible aux rôles `operateur`/`admin`) → app "Résultats des Nuits d'Étude".
- "Tableau de bord CPAP" (port 8502, visible aux rôles `medecin`/`admin`) → dashboard CPAP.

Depuis l'app "Résultats des Nuits d'Étude", le bouton **Valider le diagnostic (génère le PDF)** appelle `POST /api/analytique/resultats-nuit/:id_nuit/valider` sur l'Api Express (nécessite donc l'Api démarrée sur `http://localhost:3000`) : celle-ci recalcule les indicateurs depuis les capteurs, met à jour `resultat_nuit`, synchronise la galaxie analytique, puis génère le dossier patient en PDF (`Api/models/dossierPatientPdf.js`) sous `Api/data/dossiers-patients/dossier-patient-{id_patient}-nuit-{id_nuit}.pdf` — en y intégrant les courbes de la nuit (SpO2, débit nasal, ronflements) si elles ont déjà été produites par l'ETL Python dans `Etl/outputs`. Le chemin du PDF est renvoyé dans la réponse JSON ; il n'existe pas encore de route pour le télécharger depuis le Front. Le bouton **Ouvrir la fiche patient dans CliniquePlus** ramène vers le Front Angular (`http://localhost:4200`).

Et pour rejouer le mini ETL CPAP (lit `etl2/raw_cpap/*.csv`, alimente `faits_suivi_cpap_jour`) :
```bash
cd etl2
python3 extract2.py && python3 transform2.py && python3 load2.py
```