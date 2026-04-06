"""
Tests unitaires pour les routes de collecte.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from serveur.appli import creer_application


def test_creer_session(client):
    """POST /api/sessions doit creer une session."""
    reponse = client.post('/api/sessions', json={
        'id_session': 'test-session-1',
        'type_appareil': 'ordinateur',
        'largeur_ecran': 1920,
        'hauteur_ecran': 1080,
        'navigateur': 'Chrome 120',
        'page_consultee': '/actualites'
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


def test_enregistrer_evenements_session_inexistante(client):
    """POST /api/evenements avec session inexistante doit retourner erreur 404."""
    reponse = client.post('/api/evenements', json={
        'id_session': 'session-qui-nexiste-pas',
        'evenements': [
            {'id_contenu': 'banniere-1', 'pourcentage_visibilite': 0.5}
        ]
    })
    assert reponse.status_code == 404


def test_pourcentage_superieur_a_1(client):
    """pourcentage_visibilite > 1 doit retourner erreur 400."""
    client.post('/api/sessions', json={
        'id_session': 'test-pv',
        'type_appareil': 'ordinateur'
    })
    reponse = client.post('/api/evenements', json={
        'id_session': 'test-pv',
        'evenements': [
            {'id_contenu': 'banniere-1', 'pourcentage_visibilite': 1.5}
        ]
    })
    assert reponse.status_code == 400


def test_pourcentage_negatif(client):
    """pourcentage_visibilite negatif doit retourner erreur 400."""
    client.post('/api/sessions', json={
        'id_session': 'test-pv2',
        'type_appareil': 'ordinateur'
    })
    reponse = client.post('/api/evenements', json={
        'id_session': 'test-pv2',
        'evenements': [
            {'id_contenu': 'banniere-1', 'pourcentage_visibilite': -0.1}
        ]
    })
    assert reponse.status_code == 400


def test_largeur_ecran_flottante(client):
    """largeur_ecran avec valeur flottante doit retourner erreur 400."""
    reponse = client.post('/api/sessions', json={
        'id_session': 'test-float',
        'type_appareil': 'ordinateur',
        'largeur_ecran': 1920.5
    })
    assert reponse.status_code == 400


def test_id_contenu_trop_long(client):
    """id_contenu depassant 256 caracteres doit retourner erreur 400."""
    client.post('/api/sessions', json={
        'id_session': 'test-long',
        'type_appareil': 'ordinateur'
    })
    reponse = client.post('/api/evenements', json={
        'id_session': 'test-long',
        'evenements': [
            {'id_contenu': 'x' * 257, 'pourcentage_visibilite': 0.5}
        ]
    })
    assert reponse.status_code == 400


def test_page_actualites(client):
    """GET /actualites doit retourner 200."""
    reponse = client.get('/actualites')
    assert reponse.status_code == 200


def test_redirection_racine(client):
    """GET / doit rediriger vers /actualites."""
    reponse = client.get('/')
    assert reponse.status_code in (301, 302)
    assert '/actualites' in reponse.headers.get('Location', '')
