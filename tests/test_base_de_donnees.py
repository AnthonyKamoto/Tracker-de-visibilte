"""
Tests unitaires pour le module base_de_donnees.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from serveur.base_de_donnees import initialiser_bdd, obtenir_connexion


@pytest.fixture(autouse=True)
def bdd_propre(bdd_temporaire):
    """Initialise la BDD temporaire avant chaque test."""
    initialiser_bdd()
    yield


def test_creation_fichier_bdd(bdd_temporaire):
    """Le fichier de base de donnees doit exister apres initialisation."""
    assert os.path.exists(bdd_temporaire)


def test_table_sessions_existe():
    """La table sessions doit exister."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'")
    assert curseur.fetchone() is not None
    connexion.close()


def test_table_evenements_existe():
    """La table evenements_visibilite doit exister."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='evenements_visibilite'")
    assert curseur.fetchone() is not None
    connexion.close()


def test_colonnes_sessions():
    """La table sessions doit avoir les bonnes colonnes."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("PRAGMA table_info(sessions)")
    colonnes = [col[1] for col in curseur.fetchall()]
    attendues = ['id_session', 'type_appareil', 'largeur_ecran', 'hauteur_ecran', 'navigateur', 'page_consultee', 'date_debut']
    for col in attendues:
        assert col in colonnes
    connexion.close()


def test_colonnes_evenements():
    """La table evenements_visibilite doit avoir les bonnes colonnes."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("PRAGMA table_info(evenements_visibilite)")
    colonnes = [col[1] for col in curseur.fetchall()]
    attendues = ['id_evenement', 'id_session', 'id_contenu', 'type_contenu',
                 'pourcentage_visibilite', 'duree_exposition_ms', 'horodatage_debut',
                 'horodatage_fin', 'date_enregistrement']
    for col in attendues:
        assert col in colonnes
    connexion.close()


def test_insertion_session():
    """On doit pouvoir inserer une session."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO sessions (id_session, type_appareil) VALUES (?, ?)",
        ('s1', 'ordinateur')
    )
    connexion.commit()
    curseur.execute("SELECT * FROM sessions WHERE id_session = 's1'")
    ligne = curseur.fetchone()
    assert ligne is not None
    assert ligne['type_appareil'] == 'ordinateur'
    connexion.close()


def test_insertion_evenement():
    """On doit pouvoir inserer un evenement lie a une session."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO sessions (id_session, type_appareil) VALUES (?, ?)", ('s2', 'mobile'))
    curseur.execute(
        "INSERT INTO evenements_visibilite (id_session, id_contenu, pourcentage_visibilite) VALUES (?, ?, ?)",
        ('s2', 'banniere-1', 0.85)
    )
    connexion.commit()
    curseur.execute("SELECT * FROM evenements_visibilite WHERE id_contenu = 'banniere-1'")
    ligne = curseur.fetchone()
    assert ligne is not None
    assert ligne['pourcentage_visibilite'] == 0.85
    connexion.close()
