"""
Tests d'intégration pour le flux complet de réservation.
Ce module teste le flux complet de réservation, de la connexion à la confirmation,
en vérifiant que les points et places sont correctement mis à jour.
"""

import pytest
from gudlft.server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    """Fixture pour le client de test Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_booking_flow(client):
    """
    AJOUT: Test du flux complet de réservation.
    Vérifie l'intégration de bout en bout du processus de réservation:
    1. Connexion avec un email valide
    2. Récupération des données initiales
    3. Réservation de places
    4. Vérification que les points ont été déduits
    5. Vérification que les places disponibles ont été mises à jour
    """
    # 1. Connexion
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True
    )
    assert response.status_code == 200

    # 2. Récupérer les données initiales
    initial_clubs = loadClubs()
    initial_comps = loadCompetitions()

    initial_points = next(
        club["points"] for club in initial_clubs if club["name"] == "Simply Lift"
    )

    initial_places = next(
        comp["numberOfPlaces"]
        for comp in initial_comps
        if comp["name"] == "Spring Festival"
    )

    # 3. Réserver des places
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "2"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # 4. Vérifier que les points ont été déduits
    updated_clubs = loadClubs()
    updated_points = next(
        club["points"] for club in updated_clubs if club["name"] == "Simply Lift"
    )
    assert (
        updated_points == initial_points - 2
    )  # AMÉLIORATION: Vérification précise de la déduction des points

    # 5. Vérifier que les places ont été mises à jour
    updated_comps = loadCompetitions()
    updated_places = next(
        comp["numberOfPlaces"]
        for comp in updated_comps
        if comp["name"] == "Spring Festival"
    )
    assert (
        updated_places == initial_places - 2
    )  # AMÉLIORATION: Vérification précise de la mise à jour des places


def test_multiple_bookings_limit(client):
    """
    AJOUT: Test de la limite de réservations multiples.
    Vérifie que le système applique correctement la règle des 12 places maximum
    par club et par compétition, même sur plusieurs réservations successives.
    Nouvelle règle implémentée selon les spécifications du projet.
    """
    # Première réservation de 7 places
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "7"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # Seconde réservation de 6 places (dépasserait la limite)
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "6"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Error: Cannot book more than 12 places" in response.data
