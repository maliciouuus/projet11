# GUDLFT - Système de Gestion des Compétitions de Clubs

## Description du Projet

GUDLFT (Good Lift) est une application web développée avec Flask qui permet aux clubs de s'inscrire et de réserver des places pour des compétitions d'haltérophilie. Cette version est une amélioration majeure du [code original](https://github.com/OpenClassrooms-Student-Center/Python_Testing) avec de nombreuses nouvelles fonctionnalités et corrections.

### Fonctionnalités Principales

- **Interface utilisateur intuitive** pour la connexion des clubs et la réservation de places
- **Gestion intelligente des compétitions** avec filtrage automatique des événements passés
- **Système de points** permettant aux clubs de réserver des places selon leurs points disponibles
- **Validation complète des données** pour prévenir les erreurs et assurer l'intégrité des données
- **API RESTful** pour accéder aux informations sur les points des clubs
- **Interface de performance** permettant de surveiller les performances de l'application

## Améliorations Majeures par Rapport à la Version Originale

### 1. Architecture
- Restructuration en package Python avec une séparation claire des responsabilités
- Organisation modulaire facilitant la maintenance et l'extension
- Scripts dédiés pour l'exécution et les tests

### 2. Fonctionnalités Métier
- Gestion des compétitions passées (filtrage automatique des événements expirés)
- Limite de 12 places par club et par compétition
- Système de traçabilité des réservations
- API RESTful avec cache pour les points des clubs

### 3. Gestion des Erreurs
- Traitement robuste des erreurs avec try/except
- Validation complète des données utilisateur
- Handlers personnalisés pour les erreurs 404 et 500
- Gestion des fichiers manquants ou corrompus

### 4. Performance
- Mise en cache pour l'API
- Optimisation des recherches avec `next()`
- Conversion cohérente des types de données

### 5. Tests
- Tests unitaires exhaustifs
- Tests d'intégration
- Tests de performance avec Locust
- Configuration pour une couverture à 100%

## Structure du Projet

```
gudlft/                  # Package principal
├── __init__.py          # Initialisation du package
├── server.py            # Application Flask principale
└── templates/           # Templates HTML

tests/                   # Tests
├── integration_tests/   # Tests d'intégration
├── performance_tests/   # Tests de performance avec Locust
├── unit_tests/          # Tests unitaires
└── conftest.py          # Configuration pytest

# Fichiers de configuration et d'exécution
run.py                   # Script d'exécution principal
setup.py                 # Configuration du package
requirements.txt         # Dépendances
run_tests.sh             # Script pour exécuter les tests
run.sh                   # Script pour exécuter l'application
.coveragerc              # Configuration de la couverture des tests

# Données
clubs.json               # Données des clubs
competitions.json        # Données des compétitions
bookings.json            # Données des réservations
```

## Prérequis

- Python 3.6+
- pip
- virtualenv (recommandé)

## Installation

1. Cloner le dépôt :
   ```bash
   git clone <URL_DU_REPO>
   cd gudlft
   ```

2. Créer et activer un environnement virtuel (recommandé) :
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Installer le package en mode développement :
   ```bash
   pip install -e .
   ```

## Utilisation

### Lancer l'Application

```bash
python run.py
```
ou utilisez le script shell fourni :
```bash
./run.sh
```

L'application sera accessible à l'adresse `http://localhost:5000`

### Exécuter les Tests

Pour lancer tous les tests :
```bash
./run_tests.sh
```

Pour lancer uniquement les tests unitaires :
```bash
python -m pytest tests/unit_tests
```

Pour lancer les tests de performance :
```bash
python -m locust -f tests/performance_tests/test_locust.py
```

## API

L'application expose une API RESTful pour accéder aux points des clubs :

- **Endpoint** : `/api/points`
- **Méthode** : GET
- **Format de réponse** : JSON
- **Exemple de réponse** :
  ```json
  {
    "clubs": [
      {"name": "Simply Lift", "points": 10},
      {"name": "Iron Temple", "points": 5},
      {"name": "She Lifts", "points": 12}
    ]
  }
  ```

## Contribuer

1. Forker le projet
2. Créer une branche pour votre fonctionnalité : `git checkout -b feature/nouvelle-fonctionnalite`
3. Commiter vos changements : `git commit -m 'Ajout de la nouvelle fonctionnalité'`
4. Pousser vers la branche : `git push origin feature/nouvelle-fonctionnalite`
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Auteurs

- Développeur initial - [OpenClassrooms](https://github.com/OpenClassrooms-Student-Center)
- Améliorations et refactoring - Sacha
