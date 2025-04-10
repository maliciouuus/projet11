"""
Package GUDLFT pour la gestion des compétitions de clubs.

--------------------------------------------------------------------------------
AMÉLIORATION STRUCTURELLE PAR RAPPORT AU REPOSITORY ORIGINAL:
--------------------------------------------------------------------------------
Le code original était organisé de manière monolithique, avec un seul fichier
server.py à la racine du projet. Cette nouvelle organisation en package Python 
offre plusieurs avantages:

1. Architecture modulaire et extensible:
   - Séparation claire des responsabilités
   - Facilité d'ajout de nouveaux modules sans modifier l'existant
   - Meilleure lisibilité et maintenabilité du code

2. Installation en tant que package Python:
   - Possibilité d'installer l'application avec pip (-e . pour le mode développement)
   - Structure standardisée reconnue par les outils Python
   - Résolution des problèmes d'import dans les tests

3. Bonnes pratiques de développement:
   - Structure conforme aux standards de développement Python
   - Importation simplifiée des composants dans d'autres modules
   - Compatibilité avec les outils d'analyse de code et de test

Cette réorganisation a permis de transformer un simple script en une application
structurée et professionnelle, tout en maintenant la compatibilité avec le code
original.
--------------------------------------------------------------------------------
"""

# GUDLFT package
# Cette directive permet l'import du module server et de ses fonctionnalités
# La structure en package facilite l'organisation du code et permet un import plus propre

# Import explicite des éléments les plus utilisés pour les rendre disponibles directement
# depuis le package principal (import gudlft) sans avoir à spécifier le sous-module
from .server import app, loadClubs, loadCompetitions
