#!/bin/bash

# Couleurs pour une meilleure lisibilité
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Port par défaut pour Locust
LOCUST_PORT=8089
# Port par défaut pour Flask
FLASK_PORT=5000

# Fonction pour afficher l'aide
show_help() {
    echo "Usage: $0 [-p port] [-f flask_port]"
    echo "Options:"
    echo "  -p PORT        Spécifier un port pour Locust (défaut: 8089)"
    echo "  -f FLASK_PORT  Spécifier un port pour Flask (défaut: 5000)"
    echo "  -h             Afficher cette aide"
}

# Traitement des arguments
while getopts "p:f:h" opt; do
    case ${opt} in
        p )
            LOCUST_PORT=$OPTARG
            ;;
        f )
            FLASK_PORT=$OPTARG
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

# Variable pour stocker le PID du serveur Flask
FLASK_PID=""

# Fonction pour démarrer le serveur Flask
start_flask_server() {
    echo -e "${BLUE}=== Démarrage du serveur Flask sur le port $FLASK_PORT ===${NC}\n"
    export FLASK_APP=run.py
    export FLASK_ENV=development
    python3 -m flask run --port=$FLASK_PORT > flask_server.log 2>&1 &
    FLASK_PID=$!
    echo -e "${GREEN}Serveur Flask démarré avec PID: $FLASK_PID${NC}"
    echo -e "${YELLOW}Attente de 5 secondes pour laisser le serveur démarrer...${NC}"
    sleep 5
}

# Fonction pour arrêter le serveur Flask
stop_flask_server() {
    if [ ! -z "$FLASK_PID" ]; then
        echo -e "${BLUE}=== Arrêt du serveur Flask (PID: $FLASK_PID) ===${NC}\n"
        kill $FLASK_PID 2>/dev/null || true
        echo -e "${GREEN}Serveur Flask arrêté${NC}"
    fi
}

# Fonction pour exécuter les tests unitaires et d'intégration
run_unit_integration_tests() {
    echo -e "${BLUE}=== Exécution des tests pour 100% de couverture ===${NC}\n"

    # Nettoyage des fichiers de cache Python et de couverture
    echo -e "${BLUE}Nettoyage des fichiers temporaires...${NC}"
    find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    find . -type f -name ".coverage" -delete
    find . -type d -name "htmlcov" -exec rm -r {} + 2>/dev/null || true

    # Exécution de tous les tests disponibles avec la verbosité
    echo -e "${BLUE}\nExécution des tests...${NC}"
    python3 -m pytest tests/ -v

    # Génération du rapport de couverture
    echo -e "${BLUE}\nGénération du rapport de couverture...${NC}"
    python3 -m pytest tests/ --cov=gudlft --cov-config=.coveragerc --cov-report=term
    python3 -m pytest tests/ --cov=gudlft --cov-config=.coveragerc --cov-report=html

    echo -e "\n${GREEN}Tests terminés. Ouvrez htmlcov/index.html pour voir le rapport détaillé.${NC}"
}

# Fonction pour lancer Locust
run_locust() {
    echo -e "${BLUE}=== Démarrage des tests de performance avec Locust ===${NC}\n"
    
    echo -e "${YELLOW}Démarrage de Locust sur le port $LOCUST_PORT${NC}"
    echo -e "${YELLOW}Interface web disponible à: http://localhost:$LOCUST_PORT${NC}"
    echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter Locust${NC}\n"
    
    python3 -m locust -f tests/performance_tests/test_locust.py --web-port=$LOCUST_PORT --host=http://localhost:$FLASK_PORT
}

# Fonction pour lancer Locust en mode headless
run_locust_headless() {
    echo -e "${BLUE}=== Démarrage des tests de performance avec Locust (mode headless) ===${NC}\n"
    
    echo -e "${YELLOW}Exécution de Locust en mode headless avec 6 utilisateurs${NC}"
    echo -e "${YELLOW}La durée du test est de 30 secondes${NC}\n"
    
    python3 -m locust -f tests/performance_tests/test_locust.py --headless -u 6 -r 1 --run-time 30s --host=http://localhost:$FLASK_PORT
}

# Fonction pour générer un rapport Flake8
generate_flake8_report() {
    echo -e "${BLUE}=== Génération du rapport Flake8 ===${NC}\n"
    
    # Vérifier si le répertoire reports existe, sinon le créer
    if [ ! -d "reports" ]; then
        mkdir -p reports
    fi
    
    # Générer le rapport HTML
    echo -e "${BLUE}Analyse du code avec Flake8...${NC}"
    python3 -m flake8 --format=html --htmldir=reports/flake8 gudlft/ tests/
    
    echo -e "\n${GREEN}Rapport Flake8 généré avec succès.${NC}"
    echo -e "${GREEN}Le rapport est disponible dans: reports/flake8/index.html${NC}"
    
    # Afficher un résumé des problèmes trouvés
    echo -e "\n${BLUE}Résumé des problèmes Flake8:${NC}"
    python3 -m flake8 gudlft/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
    python3 -m flake8 gudlft/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics
}

# Assurer que le serveur Flask est arrêté à la fin du script
trap stop_flask_server EXIT

# Activation de l'environnement virtuel si présent
if [ -d "env" ]; then
    echo -e "${BLUE}Activation de l'environnement virtuel...${NC}"
    source env/bin/activate
fi

# Installation/Mise à jour des dépendances
echo -e "${BLUE}Installation/Mise à jour des dépendances...${NC}"
pip install -r requirements.txt >/dev/null 2>&1

# Installation du package en mode développement si ce n'est pas déjà fait
if [ ! -d "gudlft.egg-info" ]; then
    echo -e "${BLUE}Installation du package en mode développement...${NC}"
    pip install -e . >/dev/null 2>&1
fi

# Menu principal
clear
echo -e "${GREEN}=======================================================${NC}"
echo -e "${GREEN}=== Tests et Performance pour l'application GUDLFT ===${NC}"
echo -e "${GREEN}=======================================================${NC}"
echo ""
echo -e "${BLUE}Choisissez une option :${NC}"
echo ""
echo "1) Exécuter les tests unitaires et d'intégration"
echo "2) Lancer Locust (interface web)"
echo "3) Lancer Locust (mode headless)"
echo "4) Générer un rapport Flake8"
echo "5) Quitter"
echo ""
read -p "Votre choix (1-5) : " choice

case $choice in
    1)
        run_unit_integration_tests
        ;;
    2)
        start_flask_server
        run_locust
        # Le serveur Flask sera arrêté par le trap EXIT
        ;;
    3)
        start_flask_server
        run_locust_headless
        # Le serveur Flask sera arrêté par le trap EXIT
        ;;
    4)
        generate_flake8_report
        ;;
    5)
        echo -e "${GREEN}Au revoir !${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Choix invalide !${NC}"
        exit 1
        ;;
esac 