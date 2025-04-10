"""
Fixtures communes pour les tests de l'application GUDLFT.
"""

import pytest
import json
from gudlft.server import app
from datetime import datetime, timedelta


@pytest.fixture
def client():
    """
    Fixture créant un client de test Flask.
    """
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "localhost"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        client.environment_preserve_context = True
        client.follow_redirects = True
        yield client


@pytest.fixture
def clubs():
    """
    Fixture fournissant des données de clubs de test.
    """
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": 4},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": 12},
    ]


@pytest.fixture
def competitions():
    """
    Fixture fournissant des données de compétitions de test.
    """
    # Calculate future dates for competitions
    future_date1 = datetime.now() + timedelta(days=30)
    future_date2 = datetime.now() + timedelta(days=60)
    past_date = datetime.now() - timedelta(days=1)

    return [
        {
            "name": "Spring Festival",
            "date": future_date1.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": 25,
        },
        {
            "name": "Fall Classic",
            "date": future_date2.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": 13,
        },
        {
            "name": "Past Competition",
            "date": past_date.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": 13,
        },
    ]


@pytest.fixture(autouse=True)
def setup_test_data(clubs, competitions):
    """
    Fixture qui prépare les données de test avant chaque test
    et nettoie après.
    """
    # Sauvegarde des données de test
    with open("clubs.json", "w") as f:
        json.dump(
            {"clubs": [{**club, "points": str(club["points"])} for club in clubs]}, f
        )

    with open("competitions.json", "w") as f:
        json.dump(
            {
                "competitions": [
                    {**comp, "numberOfPlaces": str(comp["numberOfPlaces"])}
                    for comp in competitions
                ]
            },
            f,
        )

    # Réinitialiser les réservations
    with open("bookings.json", "w") as f:
        json.dump({}, f)

    yield

    # Nettoyage après chaque test
    with open("clubs.json", "w") as f:
        json.dump(
            {"clubs": [{**club, "points": str(club["points"])} for club in clubs]}, f
        )

    with open("competitions.json", "w") as f:
        json.dump(
            {
                "competitions": [
                    {**comp, "numberOfPlaces": str(comp["numberOfPlaces"])}
                    for comp in competitions
                ]
            },
            f,
        )

    # Réinitialiser les réservations
    with open("bookings.json", "w") as f:
        json.dump({}, f)
