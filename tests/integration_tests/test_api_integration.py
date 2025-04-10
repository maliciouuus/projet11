"""
Tests d'intégration pour l'API des points.
Ce module vérifie que l'API des points reflète correctement les changements effectués
dans l'application, comme les déductions de points suite aux réservations.

--------------------------------------------------------------------------------
AJOUT PAR RAPPORT AU REPOSITORY ORIGINAL:
--------------------------------------------------------------------------------
Le code original:
- Ne comportait aucun test
- Ne disposait pas d'API pour accéder aux données des clubs

Ces tests d'intégration ont été ajoutés pour:

1. Vérifier le bon fonctionnement de l'API des points nouvellement créée
   - API RESTful renvoyant des données au format JSON
   - Mise en cache pour optimiser les performances

2. Tester l'intégration entre le système de réservation et l'API
   - Vérifier que les mises à jour des points (après réservation) sont reflétées dans l'API
   - S'assurer que les données sont cohérentes entre les différentes parties de l'application

3. Garantir la fiabilité de l'API pour les utilisateurs externes
   - Format de données consistant
   - Types de données corrects (entiers pour les points)
   - Réponses prévisibles et documentées

Cette fonctionnalité et ces tests étaient une exigence spécifique de la phase 2
du projet, permettant à l'application d'exposer ses données via une interface
programmable standardisée.
--------------------------------------------------------------------------------
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


def test_api_points_reflects_changes(client):
    """
    AJOUT: Test que l'API reflète les modifications des points.
    Vérifie que l'API renvoie les points mis à jour après une réservation.
    Ce test s'assure que:
    1. Les points initiaux sont récupérés via l'API
    2. Une réservation est effectuée, ce qui devrait réduire les points
    3. L'API renvoie bien les points mis à jour
    
    Cette fonctionnalité fait partie des exigences de la phase 2 pour fournir
    une API RESTful permettant l'accès aux données des clubs.
    """
    # 1. Vérifier les points initiaux via l'API
    response = client.get('/api/points')
    data = json.loads(response.data)
    initial_points = next(
        club['points'] 
        for club in data['clubs']
        if club['name'] == 'Simply Lift'
    )
    
    # 2. Faire une réservation
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '3'
    })
    
    # 3. Vérifier que l'API renvoie les points mis à jour
    response = client.get('/api/points')
    data = json.loads(response.data)
    updated_points = next(
        club['points'] 
        for club in data['clubs']
        if club['name'] == 'Simply Lift'
    )
    
    # Vérifier que les points ont été mis à jour
    assert isinstance(updated_points, int)  # Vérification du type de données
    assert updated_points < initial_points  # Points devraient diminuer après réservation 