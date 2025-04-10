"""
Tests unitaires pour le serveur principal de l'application GUDLFT.
Ce module teste les fonctionnalités de base du serveur, notamment le chargement et la sauvegarde des données,
ainsi que la vérification des compétitions ouvertes.
"""

import pytest
import json
from gudlft.server import (
    app, loadClubs, loadCompetitions, saveClubs, saveCompetitions,
    is_competition_open
)
from datetime import datetime, timedelta


@pytest.fixture
def client():
    """Fixture pour le client de test Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_load_clubs():
    """
    Test de chargement des clubs.
    AMÉLIORATION: Vérifie que les points sont correctement convertis en entiers.
    """
    clubs = loadClubs()
    assert isinstance(clubs, list)
    assert all(isinstance(club['points'], int) for club in clubs)  # Vérifie la conversion des points en entiers


def test_load_competitions():
    """
    Test de chargement des compétitions.
    AMÉLIORATION: Vérifie que les places sont correctement converties en entiers.
    """
    competitions = loadCompetitions()
    assert isinstance(competitions, list)
    assert all(isinstance(comp['numberOfPlaces'], int) for comp in competitions)  # Vérifie la conversion des places en entiers


def test_save_clubs(tmp_path):
    """
    Test de sauvegarde des clubs.
    AMÉLIORATION: Vérifie que les points sont correctement reconvertis en chaînes pour le JSON.
    """
    test_clubs = [{'name': 'Test Club', 'email': 'test@test.com', 'points': 10}]
    saveClubs(test_clubs)
    with open('clubs.json') as f:
        saved = json.load(f)
    assert isinstance(saved['clubs'][0]['points'], str)  # Vérifie que les points sont stockés comme chaînes dans le JSON


def test_save_competitions(tmp_path):
    """
    Test de sauvegarde des compétitions.
    AMÉLIORATION: Vérifie que les places sont correctement reconverties en chaînes pour le JSON.
    """
    test_comps = [{
        'name': 'Test Competition',
        'date': '2024-01-01',
        'numberOfPlaces': 20
    }]
    saveCompetitions(test_comps)
    with open('competitions.json') as f:
        saved = json.load(f)
    assert isinstance(saved['competitions'][0]['numberOfPlaces'], str)  # Vérifie que les places sont stockées comme chaînes dans le JSON


def test_is_competition_open_valid():
    """
    AJOUT: Test de vérification si une compétition est ouverte.
    Vérifie qu'une compétition avec une date future est considérée comme ouverte.
    """
    future_date = datetime.now() + timedelta(days=30)
    future_comp = {'date': future_date.strftime("%Y-%m-%d %H:%M:%S")}
    assert is_competition_open(future_comp) is True


def test_is_competition_open_invalid():
    """
    AJOUT: Test de vérification pour une compétition passée.
    Vérifie qu'une compétition avec une date passée est considérée comme fermée.
    """
    past_comp = {'date': '2020-01-01 12:00:00'}
    assert is_competition_open(past_comp) is False 