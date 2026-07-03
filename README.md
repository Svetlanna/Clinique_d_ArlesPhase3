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

## Utilisation

| N° étape | Description | Illustration |
| --- | --- | --- |
| 1 | L'utilisateur est initialement rendu sur une page de connexion lui demandant d'indiquer ses identifiants de connexions | | 
| 2 | Un tableau de bord d'accueil est affiché à l'utilisateur mentionnant quelques informations général sur la clinique et son profil | |
| 3 | L'utilisateur peut se rendre aux pages accessible pour son rôle | |

## UML / Diagramme d'utilisation

# Installation
### 1. Initialiser les bases de données
Ce projet dipose de deux bases de données relationnelles SQL :
- Un datalake sqlite3 analytique avec un modèle en galaxie/constellation
- Une base de données SQL accessible à l'aide MySQL Workbench

Ces bases de données au cours du projet seront ammenés à intéragir avec l'application opérateur/médecin et à évoluer, il est nécessaire en amont de bien les initialiser.

- Lancer la transaction comprise dans ce fichier : [Lien vers le script](ETL/script.sql) dans un onglet d'exécution de script SQL au sein de votre schéma vierge afin de recevoir les informations (tables, procédurés, vues...) du schéma.

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
source .venv/Scripts/activate
python3 -m pip install -r requirements.txt
```
### 3. Lancer le projet

Pareil que précedemment, positionnez vous à la racine de votre projet, et dans 2 terminal différents veuillez executer ces commandes afin de lancer la SPA angular & l'api Express:
```bash
cd Api/
nodemon
```

```bash
cd Front/
ng serve
```