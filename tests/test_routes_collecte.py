"""
Tests unitaires pour les routes de collecte.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from serveur.appli import creer_application


@pytest.fixture
def client(bdd_temporaire):
    """Client de test Flask."""
    appli = creer_application()
    appli.config['TESTING'] = True
    with appli.test_client() as client:
        yield client


def test_creer_session(client):
    """POST /api/sessions doit creer une session."""
    reponse = client.post('/api/sessions', json={
        'id_session': 'test-session-1',
        'type_appareil': 'ordinateur',
        'largeur_ecran': 1920,
        'hauteur_ecran': 1080,
        'navigateur': 'Chrome 120',
        'page_consultee': '/demo'
    })
    assert reponse.status_code == 201
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert donnees['id_session'] == 'test-session-1'


def test_creer_session_sans_donnees(client):
    """POST /api/sessions sans JSON doit retourner erreur 400."""
    reponse = client.post('/api/sessions')
    assert reponse.status_code == 400


def test_creer_session_champ_manquant(client):
    """POST /api/sessions sans type_appareil doit retourner erreur 400."""
    reponse = client.post('/api/sessions', json={
        'id_session': 'test-session-2'
    })
    assert reponse.status_code == 400


def test_session_dupliquee(client):
    """Creer deux fois la meme session doit retourner 200 (pas d'erreur)."""
    donnees = {
        'id_session': 'test-dup',
        'type_appareil': 'mobile'
    }
    client.post('/api/sessions', json=donnees)
    reponse = client.post('/api/sessions', json=donnees)
    assert reponse.status_code == 200


def test_enregistrer_evenements(client):
    """POST /api/evenements doit enregistrer les evenements."""
    # Creer la session d'abord
    client.post('/api/sessions', json={
        'id_session': 'test-evt',
        'type_appareil': 'ordinateur'
    })
    # Envoyer des evenements
    reponse = client.post('/api/evenements', json={
        'id_session': 'test-evt',
        'evenements': [
            {
                'id_contenu': 'banniere-1',
                'type_contenu': 'banniere',
                'pourcentage_visibilite': 0.75,
                'duree_exposition_ms': 3200
            },
            {
                'id_contenu': 'texte-intro',
                'type_contenu': 'texte',
                'pourcentage_visibilite': 1.0,
                'duree_exposition_ms': 5000
            }
        ]
    })
    assert reponse.status_code == 201
    donnees = reponse.get_json()
    assert donnees['succes'] is True
    assert donnees['nombre_enregistres'] == 2


def test_enregistrer_evenements_sans_session(client):
    """POST /api/evenements sans id_session doit retourner erreur 400."""
    reponse = client.post('/api/evenements', json={
        'evenements': [{'id_contenu': 'test', 'pourcentage_visibilite': 0.5}]
    })
    assert reponse.status_code == 400


def test_enregistrer_evenements_vides(client):
    """POST /api/evenements avec liste vide doit retourner erreur 400."""
    reponse = client.post('/api/evenements', json={
        'id_session': 'test',
        'evenements': []
    })
    assert reponse.status_code == 400
