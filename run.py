"""
Script d'exécution principal pour l'application GUDLFT.
Ce script permet de lancer l'application Flask directement
sans avoir à définir de variables d'environnement manuellement.

--------------------------------------------------------------------------------
AMÉLIORATION PAR RAPPORT AU REPOSITORY ORIGINAL:
--------------------------------------------------------------------------------
Dans le repository original, il fallait:
1. Définir manuellement la variable d'environnement FLASK_APP=server.py
2. Lancer la commande 'flask run' ou 'python -m flask run'

Ce script simplifie considérablement le démarrage de l'application:
- Un seul fichier à exécuter: 'python run.py'
- Pas besoin de configurer des variables d'environnement
- Mode debug activé automatiquement pour le développement
- Import direct depuis le package gudlft (architecture modulaire)

Cette approche est plus conforme aux bonnes pratiques de développement Python
et facilite l'utilisation de l'application, notamment pour les nouveaux utilisateurs
qui n'ont pas besoin de connaître les détails de configuration de Flask.
--------------------------------------------------------------------------------
"""

# Import de l'application depuis le package gudlft
from gudlft.server import app

# Exécution de l'application en mode débogage si ce script est lancé directement
if __name__ == "__main__":
    # L'activation du mode debug permet le rechargement automatique lors des modifications
    # et affiche les erreurs de manière détaillée, ce qui est utile pour le développement
    app.run(debug=True)
