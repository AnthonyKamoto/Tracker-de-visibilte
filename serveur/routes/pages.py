"""
Routes pour servir les pages HTML (site d'actualités).
"""

from flask import Blueprint, render_template, redirect, url_for

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def accueil():
    """Redirige vers le site d'actualités."""
    return redirect(url_for('pages.actualites'))


@pages_bp.route('/actualites')
def actualites():
    """Affiche le site d'actualités avec les contenus surveillés."""
    return render_template('actualites.html')
