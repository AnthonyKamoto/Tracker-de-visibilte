"""
Tests unitaires pour les routes de statistiques.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from serveur.appli import creer_application


@pytest.fixture
def client(bdd_temporaire):
    """Client de test Flask avec des donnees de test."""
    appli = creer_application()
    appli.config['TESTING'] = True
    with appli.test_client() as c:
        # Inserer des donnees de test
        c.post('/api/sessions', json={
            'id_session': 'stat-s1',
            'type_appareil': 'ordinateur',
            'largeur_ecran': 1920,
            'hauteur_ecran': 1080,
            'navigateur': 'Chrome 120',
            'page_consultee': '/actualites'
        })
        c.post('/api/sessions', json={
            'id_session': 'stat-s2',
            'type_appareil': 'mobile',
            'largeur_ecran': 375,
            'hauteur_ecran': 812,
            'navigateur': 'Safari 17',
            'page_consultee': '/actualites'
        })
        c.post('/api/evenements', json={
            'id_session': 'stat-s1',
            'evenements': [
                {'id_contenu': 'banniere-1', 'type_contenu': 'banniere', 'pourcentage_visibilite': 0.8, 'duree_exposition_ms': 4000},
                {'id_contenu': 'banniere-2', 'type_contenu': 'banniere', 'pourcentage_visibilite': 0.5, 'duree_exposition_ms': 2000},
            ]
        })
        c.post('/api/evenements', json={
            'id_session': 'stat-s2',
            'evenements': [
                {'id_contenu': 'banniere-1', 'type_contenu': 'banniere', 'pourcentage_visibilite': 1.0, 'duree_exposition_ms': 6000},
            ]
        })
        yield c


def test_stats_contenus(client):
    """GET /api/statistiques/contenus doit retourner des stats par contenu."""
    reponse = client.get('/api/statistiques/contenus')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert len(donnees['donnees']) == 2  # banniere-1 et banniere-2


def test_stats_contenu_detail(client):
    """GET /api/statistiques/contenus/banniere-1 doit retourner le detail."""
    reponse = client.get('/api/statistiques/contenus/banniere-1')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert donnees['donnees']['nombre_vues'] == 2
    assert donnees['donnees']['visibilite_moyenne'] == 0.9  # (0.8+1.0)/2


def test_stats_contenu_inexistant(client):
    """GET contenu inexistant doit retourner 404."""
    reponse = client.get('/api/statistiques/contenus/inexistant')
    assert reponse.status_code == 404


def test_stats_sessions(client):
    """GET /api/statistiques/sessions doit retourner un resume."""
    reponse = client.get('/api/statistiques/sessions')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert donnees['donnees']['nombre_sessions'] == 2
    assert donnees['donnees']['nombre_evenements'] == 3


def test_stats_appareils(client):
    """GET /api/statistiques/appareils doit retourner la repartition."""
    reponse = client.get('/api/statistiques/appareils')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert len(donnees['donnees']) == 2  # ordinateur et mobile


def test_stats_navigateurs(client):
    """GET /api/statistiques/navigateurs doit retourner la repartition."""
    reponse = client.get('/api/statistiques/navigateurs')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert len(donnees['donnees']) == 2  # Chrome et Safari


def test_stats_bdd_vide(bdd_temporaire):
    """Les stats avec une BDD vide doivent retourner des listes vides."""
    appli = creer_application()
    appli.config['TESTING'] = True
    with appli.test_client() as c:
        reponse = c.get('/api/statistiques/contenus')
        assert reponse.status_code == 200
        donnees = reponse.get_json()
        assert donnees['donnees'] == []


def test_stats_filtrage_date(client):
    """GET /api/statistiques/contenus avec filtre date doit fonctionner."""
    reponse = client.get('/api/statistiques/contenus?date_debut=2020-01-01&date_fin=2099-12-31')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert len(donnees['donnees']) == 2

    # Avec des dates qui excluent tout
    reponse = client.get('/api/statistiques/contenus?date_debut=2099-01-01')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['donnees'] == []


def test_stats_sessions_filtrage_date(client):
    """GET /api/statistiques/sessions avec filtre date doit fonctionner."""
    reponse = client.get('/api/statistiques/sessions?date_debut=2099-01-01')
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert donnees['donnees']['nombre_sessions'] == 0
