"""
Tests unitaires complémentaires pour atteindre une couverture de 100%.
Ce module contient des tests spécifiquement conçus pour couvrir tous les cas d'erreur
et les parties du code qui ne sont pas testées par les tests fonctionnels standard.
Ces tests utilisent principalement des mocks pour simuler des conditions d'erreur.
"""

import pytest
import json
import os
from unittest.mock import patch, MagicMock, mock_open
from gudlft.server import (
    app, get_club_competition_bookings,
    save_booking, is_competition_open,
    not_found_error, internal_error
)


@pytest.fixture
def client():
    """Fixture pour le client de test Flask."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        client.environ_base['HTTP_REFERER'] = 'http://localhost/'
        yield client


def test_invalid_competition_date():
    """
    AJOUT: Test de is_competition_open avec une date de compétition invalide.
    Ce test vérifie que la fonction gère correctement les formats de date invalides
    et renvoie False pour indiquer que la compétition n'est pas ouverte.
    Ce cas spécifique n'est pas couvert par les tests fonctionnels standard.
    """
    invalid_comp = {"date": "invalid-date-format"}
    result = is_competition_open(invalid_comp)
    assert result is False


def test_get_club_competition_bookings_new_file():
    """
    AJOUT: Test de get_club_competition_bookings avec un fichier inexistant.
    Utilise un mock pour simuler un fichier manquant (FileNotFoundError) et vérifie
    que la fonction renvoie 0 comme valeur par défaut, ce qui permet à l'application
    de continuer à fonctionner même si le fichier de réservations n'existe pas encore.
    """
    with patch('builtins.open', side_effect=FileNotFoundError):
        result = get_club_competition_bookings("Test Club", "Test Competition")
        assert result == 0


def test_get_club_competition_bookings_invalid_json():
    """
    AJOUT: Test de get_club_competition_bookings avec un JSON invalide.
    Utilise un mock pour simuler un fichier JSON corrompu ou mal formaté et vérifie
    que la fonction gère cette erreur et renvoie 0 comme valeur par défaut.
    Ce test couvre un cas d'erreur important pour la robustesse de l'application.
    """
    with patch('builtins.open', mock_open(read_data="invalid json")):
        with patch('json.load', side_effect=json.JSONDecodeError("Test error", "", 0)):
            result = get_club_competition_bookings("Test Club", "Test Competition")
            assert result == 0


def test_save_booking_new_file():
    """
    AJOUT: Test de save_booking avec un fichier de réservations inexistant.
    Simule la création d'un nouveau fichier de réservations lorsqu'il n'existe pas
    et vérifie que la fonction enregistre correctement les données.
    Ce test couvre le cas où l'application est utilisée pour la première fois.
    """
    m = mock_open()
    with patch('builtins.open', side_effect=[FileNotFoundError, m()]):
        with patch('json.dump') as mock_dump:
            save_booking("Test Club", "Test Competition", 5)
            mock_dump.assert_called_once()


def test_save_booking_invalid_json():
    """
    AJOUT: Test de save_booking avec un fichier JSON invalide.
    Simule un fichier de réservations corrompu et vérifie que la fonction gère
    cette erreur en créant un nouveau fichier avec des données valides.
    Ce test renforce la robustesse de la gestion des erreurs dans l'application.
    """
    m = mock_open()
    with patch('builtins.open', side_effect=[mock_open()(read_data="invalid json"), m()]):
        with patch('json.load', side_effect=json.JSONDecodeError("Test error", "", 0)):
            with patch('json.dump') as mock_dump:
                save_booking("Test Club", "Test Competition", 5)
                mock_dump.assert_called_once()


def test_404_error_handler():
    """
    AJOUT: Test du gestionnaire d'erreur 404.
    Vérifie que le gestionnaire d'erreur 404 renvoie le bon template et code de statut.
    Ce test s'assure que l'utilisateur obtient une page d'erreur conviviale en cas d'URL invalide.
    """
    with patch('gudlft.server.render_template', return_value='404 page') as mock_render:
        error = MagicMock()
        response, status_code = not_found_error(error)
        mock_render.assert_called_with("404.html")
        assert status_code == 404


def test_500_error_handler():
    """
    AJOUT: Test du gestionnaire d'erreur 500.
    Vérifie que le gestionnaire d'erreur 500 renvoie le bon template et code de statut.
    Ce test s'assure que l'utilisateur obtient une page d'erreur conviviale en cas d'erreur serveur,
    améliorant ainsi l'expérience utilisateur même dans les situations problématiques.
    """
    with patch('gudlft.server.render_template', return_value='500 page') as mock_render:
        error = MagicMock()
        response, status_code = internal_error(error)
        mock_render.assert_called_with("500.html")
        assert status_code == 500


def test_logout(client):
    """
    AJOUT: Test de la route de déconnexion.
    Vérifie que la route /logout redirige correctement vers la page d'accueil.
    Ce test complète la couverture des routes de l'application.
    """
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200 