"""
Routes du tableau de bord.
"""

from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def tableau_de_bord():
    """Affiche le tableau de bord des statistiques."""
    return render_template('tableau_de_bord.html')
