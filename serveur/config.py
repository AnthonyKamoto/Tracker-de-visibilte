"""
Configuration de l'application Flask.
"""

import os

# Répertoire de base du projet (un niveau au-dessus de serveur/)
REPERTOIRE_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chemin vers le fichier de base de données SQLite
CHEMIN_BDD = os.path.join(REPERTOIRE_BASE, 'donnees', 'visibilite.db')

# Configuration du serveur
HOTE = '0.0.0.0'
PORT = 5000
MODE_DEBUG = False

# Délai d'attente SQLite en secondes (pour gérer les accès concurrents)
DELAI_ATTENTE_BDD = 10
