"""
Tests unitaires pour le module analyseur.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from serveur.base_de_donnees import initialiser_bdd, obtenir_connexion
from serveur.utilitaires.analyseur import (
    calculer_statistiques_contenus,
    calculer_statistiques_contenu,
    calculer_resume_sessions,
    calculer_repartition_appareils,
    calculer_repartition_navigateurs,
)


@pytest.fixture(autouse=True)
def bdd_avec_donnees(bdd_temporaire):
    """Cree une BDD avec des donnees de test."""
    initialiser_bdd()
    connexion = obtenir_connexion()
    c = connexion.cursor()
    c.execute("INSERT INTO sessions VALUES ('s1','ordinateur',1920,1080,'Chrome 120','/demo',datetime('now'))")
    c.execute("INSERT INTO sessions VALUES ('s2','mobile',375,812,'Safari 17','/demo',datetime('now'))")
    c.execute("INSERT INTO evenements_visibilite (id_session,id_contenu,type_contenu,pourcentage_visibilite,duree_exposition_ms) VALUES ('s1','img-1','image',0.8,3000)")
    c.execute("INSERT INTO evenements_visibilite (id_session,id_contenu,type_contenu,pourcentage_visibilite,duree_exposition_ms) VALUES ('s1','img-1','image',1.0,5000)")
    c.execute("INSERT INTO evenements_visibilite (id_session,id_contenu,type_contenu,pourcentage_visibilite,duree_exposition_ms) VALUES ('s2','img-2','image',0.5,2000)")
    connexion.commit()
    connexion.close()
    yield


def test_statistiques_tous_contenus():
    """Doit retourner les stats pour tous les contenus."""
    resultats = calculer_statistiques_contenus()
    assert len(resultats) == 2
    # img-1 a 2 vues, img-2 en a 1
    img1 = next(r for r in resultats if r['id_contenu'] == 'img-1')
    assert img1['nombre_vues'] == 2


def test_statistiques_contenu_specifique():
    """Doit retourner les stats pour un contenu precis."""
    resultat = calculer_statistiques_contenu('img-1')
    assert resultat is not None
    assert resultat['nombre_vues'] == 2
    assert resultat['visibilite_moyenne'] == 0.9  # (0.8+1.0)/2


def test_statistiques_contenu_inexistant():
    """Doit retourner None pour un contenu inexistant."""
    resultat = calculer_statistiques_contenu('inexistant')
    assert resultat is None


def test_resume_sessions():
    """Doit retourner le bon nombre de sessions."""
    resultat = calculer_resume_sessions()
    assert resultat['nombre_sessions'] == 2
    assert resultat['nombre_evenements'] == 3


def test_repartition_appareils():
    """Doit retourner la repartition par appareil."""
    resultats = calculer_repartition_appareils()
    assert len(resultats) == 2
    types = [r['type_appareil'] for r in resultats]
    assert 'ordinateur' in types
    assert 'mobile' in types


def test_repartition_navigateurs():
    """Doit retourner la repartition par navigateur."""
    resultats = calculer_repartition_navigateurs()
    assert len(resultats) == 2
    navs = [r['navigateur'] for r in resultats]
    assert 'Chrome 120' in navs
    assert 'Safari 17' in navs
