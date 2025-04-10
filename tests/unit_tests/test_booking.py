"""
Tests unitaires pour les fonctionnalités de réservation.
Ces tests vérifient le comportement du système de réservation avec différents scénarios:
- Réservation avec points suffisants
- Limite de places par club (max 12)
- Points insuffisants
- Club inexistant
"""

import pytest
from gudlft.server import app


@pytest.fixture
def client():
    """Fixture pour le client de test Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchase_places_with_sufficient_points(client):
    """
    AJOUT: Test de réservation avec suffisamment de points.
    Vérifie que la réservation est acceptée quand le club a assez de points.
    """
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '2'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_purchase_places_exceeds_club_limit(client):
    """
    AJOUT: Test de réservation dépassant la limite de 12 places.
    Vérifie que la réservation est refusée quand elle dépasse la limite de 12 places par club.
    Cette règle a été ajoutée selon les spécifications du projet.
    """
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '13'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Error: Cannot book more than 12 places' in response.data


def test_purchase_places_insufficient_points(client):
    """
    AJOUT: Test de réservation avec points insuffisants.
    Vérifie que la réservation est refusée quand le club n'a pas assez de points.
    Exemple: Iron Temple a 4 points mais tente d'en utiliser 5.
    """
    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Spring Festival',
        'places': '5'  # 4 points disponibles
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Error: Not enough points' in response.data


def test_book_invalid_club(client):
    """
    AJOUT: Test de réservation avec un club invalide.
    Vérifie que le système gère correctement les tentatives de réservation avec un club inexistant.
    """
    response = client.get('/book/Spring%20Festival/InvalidClub')
    # Le système doit rediriger vers la page d'accueil
    assert response.status_code == 302