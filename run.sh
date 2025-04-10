#!/bin/bash

# Couleurs pour une meilleure lisibilité
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Port par défaut
PORT=5001

# Fonction pour afficher l'aide
show_help() {
    echo "Usage: $0 [-p port]"
    echo "Options:"
    echo "  -p PORT    Spécifier un port différent (défaut: 5001)"
    echo "  -h         Afficher cette aide"
}

# Traitement des arguments
while getopts "p:h" opt; do
    case ${opt} in
        p )
            PORT=$OPTARG
            ;;
        h )
            show_help
            exit 0
            ;;
        \? )
            echo "Option invalide: -$OPTARG" 1>&2
            show_help
            exit 1
            ;;
    esac
done

echo -e "${BLUE}=== Démarrage de l'application GUDLFT ===${NC}\n"

# Activation de l'environnement virtuel si présent
if [ -d "env" ]; then
    echo -e "${BLUE}Activation de l'environnement virtuel...${NC}"
    source env/bin/activate
fi

# Installation/Mise à jour des dépendances
echo -e "${BLUE}Installation/Mise à jour des dépendances...${NC}"
pip install -r requirements.txt

# Installation du package en mode développement si ce n'est pas déjà fait
if [ ! -d "gudlft.egg-info" ]; then
    echo -e "${BLUE}Installation du package en mode développement...${NC}"
    pip install -e .
fi

# Vérification des fichiers de données
echo -e "${BLUE}Vérification des fichiers de données...${NC}"

# Vérification de clubs.json
if [ ! -f "clubs.json" ]; then
    echo '{"clubs": [{"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}, {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}, {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}]}' > clubs.json
    echo "Fichier clubs.json créé avec des données par défaut"
fi

# Vérification de competitions.json
if [ ! -f "competitions.json" ]; then
    echo '{"competitions": [{"name": "Spring Festival", "date": "2025-03-27 10:00:00", "numberOfPlaces": "25"}, {"name": "Fall Classic", "date": "2025-10-22 13:30:00", "numberOfPlaces": "13"}]}' > competitions.json
    echo "Fichier competitions.json créé avec des données par défaut"
fi

# Vérification de bookings.json
if [ ! -f "bookings.json" ]; then
    echo '{}' > bookings.json
    echo "Fichier bookings.json créé"
fi

# Configuration de Flask
export FLASK_APP=run.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_RUN_PORT=$PORT

# Vérification si le port est disponible
if ! nc -z localhost $PORT 2>/dev/null; then
    # Démarrage du serveur Flask
    echo -e "\n${GREEN}=== Application prête ! ===${NC}"
    echo -e "Vous pouvez accéder à l'application sur http://127.0.0.1:$PORT"
    echo -e "Pour arrêter le serveur, appuyez sur Ctrl+C\n"
    python3 run.py
else
    echo -e "\n${RED}Erreur: Le port $PORT est déjà utilisé.${NC}"
    echo -e "Utilisez une des options suivantes:"
    echo -e "1. Spécifiez un autre port avec l'option -p: ./run.sh -p 5002"
    echo -e "2. Trouvez et arrêtez le processus qui utilise le port $PORT:"
    echo -e "   sudo lsof -i :$PORT"
    echo -e "   sudo kill <PID>\n"
    exit 1
fi 