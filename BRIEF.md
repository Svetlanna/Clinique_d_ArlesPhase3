# Clinique du Sommeil d'Arles — Phase 3 : prototypes et IA Random Forest

**Statut :** Assigné
**Langue :** fr
**Auteur :** Thomas VIVIANI
**Créé le :** 29/06/26

> **De :** thomas.viviani@cliniquesommeil.fr
> **À :** team-data-ia@cliniquesommeil.fr
> **Objet :** Phase 3 — Applications métiers et briques analytiques

Bonjour la team,

Vous avez livré un pipeline ETL fiable sur des nuits complètes. Cette phase vous fait avancer sur les interfaces métiers qui l'exploitent, plus une première brique analytique simple.

## 1. Ce qui est déjà fait : rappel

Vous avez livré l'ETL1 (extraction CSV → calculs → procédure stockée → rapport + courbes → datalake). C'est la fondation de tout ce qui suit.

**Compétences mobilisées :**
- MySQL
- Algorithmique
- Git
- Big Data
- SQLite
- Data lake
- Visualisation de données
- SQL

**Référentiels**
- [2023] Certification RNCP Développeur·se en intelligence artificielle

**Ressources**
- `base_analytique_et_apps.zip`
- `Random Forest en Médecine.pdf`

**Contexte du projet**

## 2. Application Opérateur (Angular / Express)

Le besoin fonctionnel :

- Liste des nuits à traiter
- Sélection d'une nuit
- Saisie d'un commentaire
- Sélection du médecin validateur
- Déclenchement de l'ETL1

## 3. Application Résultats Nuit — obligatoire

Vous recevez `app_resultats_nuit_avec_ia.py`, qui affiche déjà la liste des nuits, le rapport et les courbes.

**Votre travail : ajouter la validation du diagnostic.**

L'application doit :

- Générer le PDF complet dans le dossier du patient
- Remplir la base analytique (galaxie SQLite) avec cette nuit : insérer une ligne dans `faits_nuits`, et synchroniser les dimensions nécessaires (`dim_patient`, `dim_nuit`, `dim_temps`) si elles n'y sont pas déjà.

Vous n'avez pas à implémenter l'archivage des événements respiratoires vers une table MySQL séparée : expliquez seulement dans votre rapport pourquoi ce serait nécessaire à terme et à quoi ressemblerait le schéma de cette table d'archive.

**Source MySQL pour chaque dimension de la galaxie**

| Dimension SQLite | Source MySQL |
|---|---|
| `dim_patient` | `patient` |
| `dim_nuit` | `nuit_etude` + `medecin`/`personnel` + `appareil` |
| `dim_temps` | calculée depuis n'importe quelle date traitée |
| `dim_comorbidite` | `comorbidite` |
| `bridge_patient_comorbidite` | `patient_comorbidite` |

## 4. Mini ETL CPAP — obligatoire

Le dashboard CPAP fourni a besoin d'être alimenté. À vous de construire le petit ETL qui le fait : un script qui lit un CSV de suivi CPAP quotidien et insère dans `faits_suivi_cpap_jour`, avec calcul des alertes (observance < 4h, IAH résiduel > 5).

Pour rester simple : pas de synchronisation de l'état « traité ou non » depuis MySQL.

Vous pouvez générer vous-mêmes un CSV de test plausible (avec un LLM par exemple) en reprenant le profil de notre patient sévère de l'ETL1 (Tessier) : quelques semaines de suivi CPAP, avec au moins une période où les seuils d'alerte se déclenchent, pour vérifier que votre ETL et le dashboard les détectent correctement.

## 5. Comprendre les deux architectures

Une fois vos deux ETL fonctionnels, vous devez être capables d'expliquer dans votre rapport pourquoi on a deux bases distinctes :

- **MySQL** : la vérité opérationnelle. C'est elle qui garantit la cohérence métier au quotidien : un patient, une nuit, un résultat, des contraintes d'intégrité (clés étrangères, unicité). C'est là que vivent les alertes en temps réel et les écritures métier (consultation, suivi, validation).
- **SQLite en modèle étoile/galaxie** : optimisée pour l'analyse, pas pour la cohérence transactionnelle. Plusieurs tables de faits entourées de dimensions partagées permettent de balayer rapidement de gros volumes pour des graphiques, des tendances, et de préparer des jeux de données pour un modèle IA : sans les contraintes ni le coût des jointures complexes d'une base normalisée, et sans bloquer les écritures opérationnelles pendant qu'on fait de l'analyse.

## 6. Applications fournies en démonstration

Deux applications complètes vous sont fournies pour vous montrer ce que la base analytique permet une fois alimentée.

**Vous n'avez pas à les reproduire** : étudiez-les, comprenez leur logique, et identifiez leurs limites (à documenter dans votre rapport).

### A. `app_resultats_nuit_avec_ia.py` + `ia_comorbidites.py`

Reprend l'application résultats nuit, et ajoute une prédiction de comorbidités probables pour le patient sélectionné.

**Principe :** entraîner sur le passé, prédire sur le présent. On n'entraîne jamais sur la nuit qu'on évalue :

- **Entraînement :** sur la galaxie SQLite, qui contient l'historique des nuits déjà validées (déjà passées par `faits_nuits`), avec leurs comorbidités connues.
- **Prédiction :** sur la nuit MySQL sélectionnée, qui, par construction, n'est pas encore dans la galaxie puisqu'elle n'a pas encore été validée.

**Fonctionnement :** un modèle RandomForest entraîné par comorbidité (les 5 plus fréquentes dans la galaxie), avec imputation des valeurs manquantes et normalisation. La comorbidité la plus probable s'affiche pour le patient sélectionné, avec un détail complet sur demande.

**Limites à identifier :**

- Peu de cas positifs par comorbidité sur une petite base : la probabilité affichée n'a pas de vraie valeur statistique tant que la base reste petite.
- Pas de split train/test : le modèle n'est jamais évalué sur des données qu'il n'a pas vues.
- Limité aux 5 comorbidités les plus fréquentes : les comorbidités plus rares ne sont jamais proposées.
- Seuils de risque (élevé/modéré/faible) codés en dur dans le fichier, pas configurables.
- Pas de retour médical réinjecté pour améliorer le modèle dans le temps.

### B. `dashboard_cpap.py`

Tableau de bord de suivi CPAP, branché sur la galaxie SQLite : vue d'ensemble, alertes, historique par patient, bilans mensuels, et un onglet de prédiction du risque d'alerte du lendemain (RandomForest), avec cette fois un vrai split 80/20 et une accuracy mesurée.

**Limites à identifier :**

- Données statiques, pas de mise à jour automatique (pas d'ETL connecté en continu depuis MySQL ou CSV).
- Un seul modèle générique pour prédire « une alerte », sans distinguer le type (observance vs IAH résiduel) — un modèle par type d'alerte serait plus précis.
- Pas de validation médicale du résultat : impossible de savoir si une prédiction passée était juste, donc impossible d'améliorer le modèle.
- Tout dans un seul fichier : logique de requêtage, IA et interface mélangées, ce qui complique la maintenance.
- Visualisations Matplotlib/Seaborn, peu interactives.
- Pas de suivi de la performance du modèle dans le temps (aucune trace des prédictions passées pour vérifier si le modèle s'améliore).
- N'interroge que SQLite, y compris pour l'alerte d'un patient individuel : une vraie alerte temps réel devrait venir de MySQL, où la donnée est fraîche. SQLite reste pertinent pour les vues d'ensemble et tendances, pas pour la détection immédiate.

Vous pouvez enrichir la galaxie vous-mêmes si vous voulez observer l'effet sur les prédictions IA.

Cordialement,
Thomas

---

## Modalités pédagogiques

**Bonus :** Faire vous-même les deux applis livrées.

**Bonus :** Intégrer `dim_suivi_patient` à la galaxie.

On a identifié ensemble que le suivi patient (poids, IMC, tension, statut tabac) est une dimension à part partagée par plusieurs faits.

Vous n'avez pas à implémenter le chargement de cette dimension. Produisez uniquement un schéma logique (diagramme) qui montre où elle s'insère dans la galaxie et quels faits s'y rattachent.

### Pour aller plus loin

**Sur l'architecture et la maintenabilité**

- Réorganiser le dashboard CPAP en plusieurs fichiers (configuration, fonctions de requêtage, module IA, interface) plutôt qu'un seul fichier.
- Remplacer les graphiques Matplotlib/Seaborn par des graphiques Plotly, interactifs (zoom, survol, thèmes).

**Sur la synchronisation des données**

- Développer un script qui synchronise automatiquement MySQL → SQLite au moment de la validation du diagnostic (plutôt qu'un ETL déclenché manuellement).
- Pour le dashboard CPAP : brancher le suivi quotidien sur une vraie synchronisation MySQL/CSV en continu plutôt que sur un chargement unique.

**Sur la rigueur du modèle IA**

- Pour le module comorbidités : ajouter un vrai split train/test pour pouvoir mesurer la performance du modèle, comme c'est déjà fait dans le dashboard CPAP.
- Prédire au-delà des 5 comorbidités les plus fréquentes.
- Rendre les seuils de risque configurables plutôt que codés en dur.
- Mettre en place un réentraînement périodique des modèles.
- Stocker les prédictions dans une table dédiée.

**Sur l'interface**

- Ajouter des graphiques supplémentaires dans la vue d'ensemble du dashboard CPAP.
- Permettre l'export des données (patients à contacter, alertes) en CSV/Excel.

## Modalités d'évaluation

Rapport et pitch oral de présentation du projet.

### Livrables

- Application Opérateur fonctionnelle (Angular/Express)
- Application Résultats Nuit complétée (validation → PDF → galaxie)
- Mini ETL CPAP fonctionnel + CSV de test
- Schéma logique de la galaxie avec `dim_suivi_patient` intégrée
- Rapport organisé par compétence du référentiel (voir ci-dessous)

### Structure attendue du rapport (par compétence du référentiel)

- **C1, C2** : extraction et requêtes SQL (rappel ETL1, mini ETL CPAP)
- **C4** : modélisation des données (schéma galaxie + `dim_suivi_patient`)
- **C5** : API/accès aux données (procédures stockées utilisées)
- **C14, C15** : analyse du besoin et conception technique (vos choix d'architecture pour les deux applications)
- **C16, C17** : réalisation technique (composants développés)
- **CT5, CT6** : partage de connaissance et présentation (synthèse claire des limites identifiées en partie 6, justification des choix)
- Ainsi que **C8, C9, C10** si traité

### Critères de performance

Dossier validant plus de 50 % du titre.
