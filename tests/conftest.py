"""
Configuration partagee pour les tests.
Redirige la base de donnees vers un fichier temporaire
afin d'eviter les conflits avec le serveur en cours d'execution.
"""

import os

import pytest


@pytest.fixture(autouse=True)
def bdd_temporaire(monkeypatch, tmp_path):
    """Redirige CHEMIN_BDD vers un fichier temporaire pour chaque test."""
    chemin_temp = str(tmp_path / "test_visibilite.db")
    monkeypatch.setattr("serveur.config.CHEMIN_BDD", chemin_temp)
    monkeypatch.setattr("serveur.base_de_donnees.CHEMIN_BDD", chemin_temp)
    yield chemin_temp
