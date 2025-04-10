"""
Flask application pour la gestion des compétitions de club GUDLFT.
Ce module fournit les fonctionnalités principales de réservation et gestion des compétitions.

--------------------------------------------------------------------------------
AMÉLIORATIONS MAJEURES PAR RAPPORT AU REPOSITORY ORIGINAL:
--------------------------------------------------------------------------------
1. ARCHITECTURE:
   - Restructuration en package Python avec __init__.py
   - Organisation claire des imports et des fonctions

2. FONCTIONNALITÉS MÉTIER:
   - Gestion des compétitions passées (filtrage des compétitions expirées)
   - Limite de 12 places par club et par compétition
   - Système de traçabilité des réservations via bookings.json
   - API RESTful des points avec cache

3. GESTION DES ERREURS:
   - Gestion robuste avec try/except pour toutes les opérations critiques
   - Traitement des cas d'erreur (fichiers manquants, données incorrectes)
   - Validation complète des données utilisateur
   - Handlers personnalisés pour les erreurs 404 et 500

4. PERFORMANCE:
   - Utilisation de cache pour l'API
   - Optimisation des recherches avec next()
   - Conversion des types de données cohérente

5. QUALITÉ DU CODE:
   - Documentation complète avec docstrings
   - Code structuré selon les bonnes pratiques PEP8
   - Tests unitaires, d'intégration et de performance
--------------------------------------------------------------------------------
"""

import json
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
)
from flask_caching import Cache  # AJOUT: Système de cache pour optimiser les performances

app = Flask(__name__)
app.secret_key = "something_special"

# AJOUT: Configuration du cache pour optimiser les performances
# Cache SimpleCache en mémoire, idéal pour le développement
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Global variables
clubs = []
competitions = []


def loadClubs():
    """
    AMÉLIORATION: Fonction de chargement des clubs avec gestion d'erreurs robuste.
    Charge les clubs depuis le fichier JSON et convertit les points en entiers.
    Gère les erreurs de fichier manquant, JSON incorrect, etc.
    
    Dans la version originale:
    - Pas de gestion d'erreurs (risque de plantage)
    - Pas de conversion des types (points stockés comme chaînes)
    - Pas de fallback en cas d'erreur
    """
    try:
        with open("clubs.json") as c:
            listOfClubs = json.load(c)["clubs"]
            # AMÉLIORATION: Conversion des points en entiers pour éviter les erreurs de type
            for club in listOfClubs:
                club["points"] = int(club["points"])
            return listOfClubs
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error loading clubs: {e}")
        # AMÉLIORATION: Retour d'une liste vide comme fallback pour éviter les crashes
        return []


def loadCompetitions():
    """
    AMÉLIORATION: Fonction de chargement des compétitions avec gestion d'erreurs robuste.
    Charge les compétitions depuis le fichier JSON et convertit les places en entiers.
    Gère les erreurs de fichier manquant, JSON incorrect, etc.
    
    Dans la version originale:
    - Pas de gestion d'erreurs (risque de plantage)
    - Pas de conversion des types (places stockées comme chaînes)
    - Pas de fallback en cas d'erreur
    """
    try:
        with open("competitions.json") as comps:
            listOfCompetitions = json.load(comps)["competitions"]
            # AMÉLIORATION: Conversion des places en entiers pour éviter les erreurs de type
            for comp in listOfCompetitions:
                comp["numberOfPlaces"] = int(comp["numberOfPlaces"])
            return listOfCompetitions
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error loading competitions: {e}")
        # AMÉLIORATION: Retour d'une liste vide comme fallback pour éviter les crashes
        return []


def saveClubs(clubs_data):
    """
    AMÉLIORATION: Fonction de sauvegarde des clubs avec conversion de types.
    Convertit les points en chaînes pour le format JSON et sauvegarde les données.
    
    Changements:
    - Création de copies des objets pour éviter la modification des originaux
    - Conversion cohérente des types (entiers -> chaînes)
    """
    # Convert points back to strings for JSON storage
    clubs_to_save = []
    for club in clubs_data:
        club_copy = club.copy()  # AMÉLIORATION: Copie pour éviter de modifier l'original
        club_copy["points"] = str(club_copy["points"])
        clubs_to_save.append(club_copy)

    with open("clubs.json", "w") as c:
        json.dump({"clubs": clubs_to_save}, c)


def saveCompetitions(competitions_data):
    """
    AMÉLIORATION: Fonction de sauvegarde des compétitions avec conversion de types.
    Convertit les places en chaînes pour le format JSON et sauvegarde les données.
    
    Changements:
    - Création de copies des objets pour éviter la modification des originaux
    - Conversion cohérente des types (entiers -> chaînes)
    """
    # Convert numberOfPlaces back to strings for JSON storage
    comps_to_save = []
    for comp in competitions_data:
        comp_copy = comp.copy()  # AMÉLIORATION: Copie pour éviter de modifier l'original
        comp_copy["numberOfPlaces"] = str(comp_copy["numberOfPlaces"])
        comps_to_save.append(comp_copy)

    with open("competitions.json", "w") as comps:
        json.dump({"competitions": comps_to_save}, comps)


def is_competition_open(competition):
    """
    AJOUT: Fonction pour vérifier si une compétition est encore ouverte (date future).
    Gère les erreurs de format de date et renvoie False si la date est invalide.
    
    Nouvelle fonctionnalité qui n'existait pas dans le code original.
    Cette fonction permet de filtrer les compétitions passées qui ne devraient
    plus être disponibles pour réservation.
    """
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        competition_date = datetime.strptime(competition["date"], date_format)
        return datetime.now() < competition_date
    except (ValueError, TypeError) as e:
        print(f"Error parsing competition date: {e}")
        return False


# Load initial data
clubs = loadClubs()
competitions = loadCompetitions()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """
    AMÉLIORATION: Route d'affichage du résumé avec validation robuste de l'email.
    Gère les erreurs et renvoie des messages d'erreur appropriés.
    Filtre les compétitions pour n'afficher que celles qui sont encore ouvertes.
    
    Changements:
    - Validation de l'email non vide
    - Recherche du club avec gestion d'erreur
    - Filtrage des compétitions passées
    - Block try/except global pour éviter les crashs
    """
    email = request.form.get("email", "").strip()

    if not email:
        flash("Please provide an email")
        return redirect(url_for("index"))

    try:
        club = next((club for club in clubs if club["email"] == email), None)
        if club:
            # AJOUT: Filtre des compétitions pour ne montrer que celles qui sont encore ouvertes
            open_competitions = [
                comp for comp in competitions if is_competition_open(comp)
            ]
            return render_template(
                "welcome.html", 
                club=club, 
                competitions=open_competitions
            )
        else:
            flash("Unknown email, please try again")
            return redirect(url_for("index"))
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    AMÉLIORATION: Route de réservation avec validation robuste.
    Vérifie l'existence du club et de la compétition.
    Vérifie si la compétition est encore ouverte avant d'autoriser la réservation.
    
    Changements:
    - Validation de l'existence du club et de la compétition
    - Vérification que la compétition n'est pas passée
    - Gestion globale des erreurs
    """
    try:
        foundClub = next((c for c in clubs if c["name"] == club), None)
        foundCompetition = next(
            (c for c in competitions if c["name"] == competition), None
        )

        if not foundClub:
            flash("Club not found")
            return redirect(url_for("index"))

        if not foundCompetition:
            flash("Competition not found")
            return redirect(url_for("index"))

        # AJOUT: Vérification si la compétition est encore ouverte
        if not is_competition_open(foundCompetition):
            flash("This competition is no longer open for booking")
            open_competitions = [
                comp for comp in competitions if is_competition_open(comp)
            ]
            return render_template(
                "welcome.html", club=foundClub, competitions=open_competitions
            )

        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    except Exception as e:
        flash(f"Something went wrong: {str(e)}")
        return redirect(url_for("index"))


def get_club_competition_bookings(club_name, competition_name):
    """
    AJOUT: Fonction pour obtenir le nombre de places déjà réservées par un club pour une compétition.
    Utilisée pour vérifier la limite de 12 places par club et par compétition.
    
    Nouvelle fonctionnalité qui n'existait pas dans le code original.
    Cette fonction permet de tracer les réservations et d'appliquer la règle
    des 12 places maximum par club et par compétition.
    """
    # Load bookings from a JSON file or create a new one if it doesn't exist
    try:
        with open("bookings.json", "r") as f:
            bookings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        bookings = {}

    # Get bookings for this club and competition
    booking_key = f"{club_name}_{competition_name}"
    return bookings.get(booking_key, 0)


def save_booking(club_name, competition_name, places):
    """
    AJOUT: Fonction pour sauvegarder une réservation.
    Permet de suivre combien de places chaque club a réservé pour chaque compétition.
    
    Nouvelle fonctionnalité qui n'existait pas dans le code original.
    Cette fonction sauvegarde l'historique des réservations dans un fichier JSON.
    """
    # Load existing bookings
    try:
        with open("bookings.json", "r") as f:
            bookings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        bookings = {}

    # Update booking
    booking_key = f"{club_name}_{competition_name}"
    current_places = bookings.get(booking_key, 0)
    bookings[booking_key] = current_places + places

    # Save bookings
    with open("bookings.json", "w") as f:
        json.dump(bookings, f)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """
    AMÉLIORATION: Route d'achat de places avec validation complète.
    Vérifie tous les cas d'erreur possibles:
    - Données manquantes ou invalides
    - Compétition fermée
    - Nombre de places invalide (négatif ou zéro)
    - Compétition complète
    - Dépassement des 12 places par club et par compétition
    - Points insuffisants
    
    Changements majeurs par rapport à l'original:
    - Validation exhaustive des données d'entrée
    - Vérification des compétitions ouvertes
    - Validation du nombre de places (positif, disponible)
    - Implémentation de la règle des 12 places maximum par club
    - Traçabilité des réservations
    - Rechargement des données pour assurer la cohérence
    """
    try:
        global clubs, competitions
        # Reload data to ensure we have the latest state
        clubs = loadClubs()
        competitions = loadCompetitions()

        competition_name = request.form.get("competition")
        club_name = request.form.get("club")
        places_str = request.form.get("places")

        if not competition_name or not club_name or not places_str:
            flash("Error: Missing required information")
            return redirect(url_for("index"))

        try:
            placesRequired = int(places_str)
        except ValueError:
            flash("Error: Invalid number of places")
            return redirect(url_for("index"))

        competition = next(
            (c for c in competitions if c["name"] == competition_name), None
        )
        club = next((c for c in clubs if c["name"] == club_name), None)

        if not competition or not club:
            flash("Error: Club or competition not found")
            return redirect(url_for("index"))

        # AJOUT: Validation que la compétition est encore ouverte
        if not is_competition_open(competition):
            flash("Error: This competition is no longer open for booking")
            open_comps = [comp for comp in competitions if is_competition_open(comp)]
            return render_template("welcome.html", club=club, competitions=open_comps)

        # AJOUT: Validation du nombre positif
        if placesRequired <= 0:
            flash("Error: Invalid number of places")
            open_comps = [comp for comp in competitions if is_competition_open(comp)]
            return render_template("welcome.html", club=club, competitions=open_comps)

        # AJOUT: Validation des places disponibles dans la compétition
        if competition["numberOfPlaces"] <= 0:
            flash("Error: Competition is full")
            open_comps = [comp for comp in competitions if is_competition_open(comp)]
            return render_template("welcome.html", club=club, competitions=open_comps)

        if placesRequired > competition["numberOfPlaces"]:
            flash("Error: Not enough places available")
            open_comps = [comp for comp in competitions if is_competition_open(comp)]
            return render_template("welcome.html", club=club, competitions=open_comps)

        # AJOUT: Validation maximum 12 places par club
        club_name = club["name"]
        comp_name = competition["name"]
        current_bookings = get_club_competition_bookings(club_name, comp_name)
        booking_total = current_bookings + placesRequired
        if booking_total > 12:
            flash("Error: Cannot book more than 12 places per competition")
            open_comps = [
                comp for comp in competitions if is_competition_open(comp)
            ]
            return render_template(
                "welcome.html", 
                club=club, 
                competitions=open_comps
            )

        # AMÉLIORATION: Validation des points suffisants
        if placesRequired > club["points"]:
            flash("Error: Not enough points")
            open_comps = [
                comp for comp in competitions if is_competition_open(comp)
            ]
            return render_template(
                "welcome.html",
                club=club,
                competitions=open_comps
            )

        # Update points and places
        club["points"] = club["points"] - placesRequired
        new_places = competition["numberOfPlaces"] - placesRequired
        competition["numberOfPlaces"] = new_places

        # AJOUT: Sauvegarde de la réservation
        save_booking(club["name"], competition["name"], placesRequired)

        # Save changes
        saveClubs(clubs)
        saveCompetitions(competitions)

        # Reload data to ensure consistency
        clubs = loadClubs()
        competitions = loadCompetitions()

        # Get updated club and competition for template
        club = next((c for c in clubs if c["name"] == club_name), None)
        open_comps = [
            comp for comp in competitions if is_competition_open(comp)
        ]

        flash("Great-booking complete!")
        return render_template(
            "welcome.html",
            club=club,
            competitions=open_comps
        )

    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect(url_for("index"))


@app.route("/points")
def displayPoints():
    """Route pour afficher les points des clubs sur une page HTML."""
    return render_template("points.html", clubs=clubs)


@app.route("/api/points")
@cache.cached(timeout=30)  # AJOUT: Cache pour 30 secondes
def api_points():
    """
    AJOUT: API endpoint pour récupérer les points des clubs.
    Implémente un cache de 30 secondes pour optimiser les performances.
    Renvoie les points des clubs au format JSON.
    
    Nouvelle fonctionnalité qui n'existait pas dans le code original.
    Cette API RESTful permet l'accès aux données des clubs au format JSON,
    avec mise en cache pour optimiser les performances.
    """
    try:
        clubs_data = loadClubs()
        clubs_points = [
            {"name": club["name"], "points": club["points"]} 
            for club in clubs_data
        ]
        return {"clubs": clubs_points}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/logout")
def logout():
    """Route de déconnexion qui redirige vers la page d'accueil."""
    return redirect(url_for("index"))


# AJOUT: Gestionnaires d'erreur pour les erreurs 404 et 500
@app.errorhandler(404)
def not_found_error(error):
    """
    AJOUT: Gestionnaire pour les erreurs 404 (page non trouvée).
    Renvoie une page d'erreur personnalisée au lieu de l'erreur standard.
    """
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """
    AJOUT: Gestionnaire pour les erreurs 500 (erreur serveur).
    Renvoie une page d'erreur personnalisée au lieu de l'erreur standard.
    """
    return render_template("500.html"), 500
