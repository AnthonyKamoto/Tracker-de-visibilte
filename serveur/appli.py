"""
Point d'entree de l'application Flask.
Systeme de mesure de visibilite de contenus Web - Fondation CCC.
"""

import os
import sys

# Ajouter le repertoire parent au chemin Python pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from serveur.config import HOTE, PORT, MODE_DEBUG, REPERTOIRE_BASE
from serveur.base_de_donnees import initialiser_bdd


def creer_application():
    """Cree et configure l'application Flask."""
    appli = Flask(
        __name__,
        template_folder=os.path.join(REPERTOIRE_BASE, 'templates'),
        static_folder=os.path.join(REPERTOIRE_BASE, 'static'),
        static_url_path='/static'
    )

    # Initialiser la base de donnees au demarrage
    initialiser_bdd()

    # Enregistrer les blueprints (routes)
    from serveur.routes.pages import pages_bp
    from serveur.routes.collecte import collecte_bp
    from serveur.routes.statistiques import statistiques_bp

    appli.register_blueprint(pages_bp)
    appli.register_blueprint(collecte_bp)
    appli.register_blueprint(statistiques_bp)

    return appli


if __name__ == '__main__':
    appli = creer_application()
    appli.run(host=HOTE, port=PORT, debug=MODE_DEBUG)
