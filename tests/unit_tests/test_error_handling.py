"""
Tests unitaires pour la gestion des erreurs.
"""

import pytest
import os
from gudlft.server import app, loadClubs, loadCompetitions


def test_loadClubs_file_not_found():
    """Test de chargement des clubs lorsque le fichier n'existe pas."""
    # Sauvegarder le fichier s'il existe
    if os.path.exists('clubs.json'):
        os.rename('clubs.json', 'clubs.json.bak')
    try:
        # Le fichier n'existe pas, devrait renvoyer une liste vide
        clubs = loadClubs()
        assert clubs == []
    finally:
        # Restaurer le fichier
        if os.path.exists('clubs.json.bak'):
            os.rename('clubs.json.bak', 'clubs.json')


def test_loadCompetitions_file_not_found():
    """Test de chargement des compétitions lorsque le fichier n'existe pas."""
    # Sauvegarder le fichier s'il existe
    if os.path.exists('competitions.json'):
        os.rename('competitions.json', 'competitions.json.bak')
    try:
        # Le fichier n'existe pas, devrait renvoyer une liste vide
        competitions = loadCompetitions()
        assert competitions == []
    finally:
        # Restaurer le fichier
        if os.path.exists('competitions.json.bak'):
            os.rename('competitions.json.bak', 'competitions.json')


def test_404_error_handler():
    """Test du gestionnaire d'erreur 404."""
    with app.test_client() as client:
        response = client.get('/nonexistent-route')
        assert response.status_code == 404
        assert b'<html' in response.data 