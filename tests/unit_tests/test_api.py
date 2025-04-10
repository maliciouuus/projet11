"""
Tests unitaires pour les fonctionnalités API.
Ce module teste la nouvelle API RESTful ajoutée à l'application pour fournir
les informations sur les points des clubs en format JSON.
"""

import pytest
import json
from gudlft.server import app


@pytest.fixture
def client():
    """Fixture pour le client de test Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_api_points_structure(client):
    """
    AJOUT: Test de la structure de réponse de l'API des points.
    Vérifie que l'API renvoie les données au format JSON approprié avec les clés attendues.
    Nouvelle fonctionnalité ajoutée selon les spécifications de la phase 2.
    """
    response = client.get('/api/points')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'clubs' in data
    assert isinstance(data['clubs'], list)
    assert all('name' in club and 'points' in club for club in data['clubs'])


def test_points_page(client):
    """
    Test de la page des points.
    Vérifie que la page HTML des points est accessible et contient les éléments attendus.
    """
    response = client.get('/points')
    assert response.status_code == 200
    assert b'<html' in response.data
    assert b'Club Points' in response.data
    assert b'Points Available' in response.data 