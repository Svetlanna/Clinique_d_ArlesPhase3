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

Ce projet consiste en un prototype de DPI complet  intégrant des briques IA pour assurer la supervision des nuits d'études au sein de la clinique du sommeil d'Arles (fictif).

## État réel du projet

Statut par brique (branche `tempdev`, au 03/07/2026) :

- **App Opérateur/Médecin (Front + Api)** : authentification, dashboard, appareils, médecins, CPAP dashboard et la page Nuits Patients (`/nuitspatients`) sont fonctionnels et branchés sur l'API MySQL. La page `test-operateur` reste routée mais n'affiche que des données statiques (doublon de Nuits Patients, à retirer du routing).
- **Résultats Nuit (Front Angular)** : page encore en mock (3 nuits codées en dur, pas d'appel API, pas de validation de diagnostic ni de génération de PDF).
- **Dashboard CPAP (Etl)** : fonctionnel via `streamlit run Etl/base-analytique-et-apps/Dashboard_CPAP/dashboard_main.py`, lit la base analytique SQLite.
- **Résultats de nuit avec IA (Etl)** : fonctionnel via `streamlit run Etl/base-analytique-et-apps/app_resultats_nuit_avec_ia.py`. Les 5 modèles de prédiction de comorbidités sont entraînés (`models/*.pkl`). Cette app Python est indépendante du Front Angular, pas encore reliée.
- **Mini ETL CPAP** (`etl2/extract2.py`, `transform2.py`, `load2.py`) : fonctionnel, calcule les alertes observance/IAH et alimente `faits_suivi_cpap_jour`. `id_patient`/`id_appareil` restent codés en dur dans `extract2.py`.
- **Base analytique SQLite** : schéma en galaxie complet (`faits_nuits`, `dim_patient`, `dim_nuit`, `dim_temps`, `dim_suivi_patient`, etc.) présent à la racine (`base_analytique.db`). Aucun diagramme du schéma n'a encore été produit.
- **Manque encore** : rapport pédagogique de fin de projet, diagramme du schéma en galaxie, et une librairie de génération PDF (absente côté `Api/package.json` comme côté Python), nécessaire pour finaliser la validation de diagnostic sur la page Résultats Nuit.

## Utilisation

| N° étape | Description | Illustration |
| --- | --- | --- |
| 1 | L'utilisateur est initialement rendu sur une page de connexion lui demandant d'indiquer ses identifiants de connexions | | 
| 2 | Un tableau de bord d'accueil est affiché à l'utilisateur mentionnant quelques informations général sur la clinique et son profil | |
| 3 | L'utilisateur peut se rendre aux pages accessible pour son rôle | |

## UML / Diagramme d'utilisation

_(non produit pour le moment)_

# Installation
### 1. Initialiser les bases de données
Ce projet dipose de deux bases de données :
- Une base MySQL opérationnelle (`cliniquearles`), utilisée par l'Api Express.
- Un datalake SQLite analytique en modèle galaxie/constellation, utilisé par les apps Streamlit du dossier `Etl/` et par la page CPAP Dashboard du Front (via `Api/models/cpapModel.js`).

**Base MySQL** : dans un schéma vierge nommé `cliniquearles`, exécutez dans l'ordre :
1. [Api/dbmigration.sql](Api/dbmigration.sql) — schéma + données de démo (dump le plus à jour, à privilégier sur `clinique2nuitsv2.sql` qui est une version antérieure du même dump).
2. [Api/storedprocedure.sql](Api/storedprocedure.sql) — procédures stockées utilisées par l'Api (`sp_compteur_*`).

`Api/auth_migration.sql` existe (colonnes `password_hash`, tables `user_role`/`refresh_token`) mais n'est **pas branché au code actuel** : `authController.js` compare encore le mot de passe en clair via la table `utilisateur`. Inutile de le jouer sauf si vous reprenez le chantier d'authentification hashée (le script `seed.js` qu'il mentionne n'existe pas non plus dans le dépôt).

**Datalake SQLite** : les fichiers `.db` sont ignorés par git (`.gitignore`), donc absents d'un clone fraîchement cloné. Il n'y a pas de script qui reconstruit le schéma complet de la galaxie depuis zéro dans ce dépôt (seul `etl2/extract2.py` sait créer/alimenter la table `faits_suivi_cpap_jour`) — récupérez un `base_analytique.db` pré-rempli auprès de l'équipe et placez-le à deux endroits :
- `base_analytique.db` à la racine (lu par les apps Streamlit de `Etl/`)
- `etl2/base_analytique.db` (lu par `Api/models/cpapModel.js` pour la page CPAP Dashboard)

Ce sont deux copies indépendantes du même fichier, sans synchronisation automatique : si vous relancez `etl2/extract2.py`, pensez à recopier le fichier mis à jour vers la racine pour que les apps Streamlit voient les nouvelles données.

### 2. Installez les dépendences :
Afin que le projet soit fonctionnel, les environnements comprenant les dépendences nécessaires au fonctionnement du projet doivent être installés.

> il est supposé que vous disposiez déja de NPM, node, nodemon et python localement. 

Positionnez-vous à la racine de votre projet et effectuez ces commandes :

```bash 
cd Api
cp .env.example .env
npm install
```
** Veuillez renseigner les bons identifiants de connexion à votre base de données MYSQL créér précédemment
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

Optionnel, les deux apps Streamlit du dossier `Etl/` (base analytique déjà initialisée requise, cf. étape 1) :
```bash
cd Etl/base-analytique-et-apps/Dashboard_CPAP
streamlit run dashboard_main.py
```
```bash
cd Etl/base-analytique-et-apps
streamlit run app_resultats_nuit_avec_ia.py
```

Et pour rejouer le mini ETL CPAP (lit `etl2/raw_cpap/*.csv`, alimente `faits_suivi_cpap_jour`) :
```bash
cd etl2
python3 extract2.py && python3 transform2.py && python3 load2.py
```