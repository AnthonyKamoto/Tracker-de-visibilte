"""
Routes pour servir les pages HTML (démo et tableau de bord).
"""

from flask import Blueprint, render_template, redirect, url_for

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def accueil():
    """Redirige vers la page de démonstration."""
    return redirect(url_for('pages.page_demo'))


@pages_bp.route('/demo')
def page_demo():
    """Affiche la page de démonstration avec les contenus à surveiller."""
    return render_template('page_demo.html')


@pages_bp.route('/tableau-de-bord')
def tableau_de_bord():
    """Affiche le tableau de bord des statistiques."""
    return render_template('tableau_de_bord.html')
