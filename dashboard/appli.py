"""
Point d'entree du tableau de bord.
Application Flask independante qui affiche les statistiques
en consommant les API du serveur principal.
"""

import os
import sys

# Ajouter le repertoire parent au chemin Python pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request
from dashboard.config import HOTE, PORT, MODE_DEBUG

REPERTOIRE_DASHBOARD = os.path.dirname(os.path.abspath(__file__))


def creer_application():
    """Cree et configure l'application Flask du tableau de bord."""
    appli = Flask(
        __name__,
        template_folder=os.path.join(REPERTOIRE_DASHBOARD, 'templates'),
        static_folder=os.path.join(REPERTOIRE_DASHBOARD, 'static'),
        static_url_path='/static'
    )

    @appli.route('/')
    def tableau_de_bord():
        """Affiche le tableau de bord des statistiques."""
        # Construire l'URL du serveur dynamiquement a partir de l'hote du navigateur
        # Permet l'acces depuis le reseau local (meme hote, port 5000)
        hote = request.host.split(':')[0]
        url_serveur = f"http://{hote}:5000"
        return render_template('tableau_de_bord.html', url_serveur=url_serveur)

    return appli


if __name__ == '__main__':
    appli = creer_application()
    print(f"[Dashboard] Demarre sur http://0.0.0.0:{PORT}")
    print(f"[Dashboard] API serveur : meme hote que le dashboard, port 5000")
    appli.run(host=HOTE, port=PORT, debug=MODE_DEBUG)
