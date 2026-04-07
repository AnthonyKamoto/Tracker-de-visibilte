"""
Routes API pour les statistiques de visibilité.
"""

import logging

from flask import Blueprint, request, jsonify
from serveur.utilitaires.analyseur import (
    calculer_statistiques_contenus,
    calculer_statistiques_contenu,
    calculer_resume_sessions,
    calculer_repartition_appareils,
    calculer_repartition_navigateurs,
)

statistiques_bp = Blueprint('statistiques', __name__)
journal = logging.getLogger(__name__)


def _extraire_filtres_date():
    """Extrait les paramètres date_debut et date_fin de la requête."""
    return request.args.get('date_debut'), request.args.get('date_fin')


@statistiques_bp.route('/api/statistiques/contenus')
def stats_contenus():
    """Retourne les statistiques agrégées par contenu."""
    try:
        date_debut, date_fin = _extraire_filtres_date()
        donnees = calculer_statistiques_contenus(date_debut, date_fin)
        return jsonify({'succes': True, 'donnees': donnees})
    except Exception as exc:
        journal.error("Erreur stats contenus : %s", exc)
        return jsonify({'succes': False, 'erreur': 'Erreur interne du serveur'}), 500


@statistiques_bp.route('/api/statistiques/contenus/<id_contenu>')
def stats_contenu_detail(id_contenu):
    """Retourne les statistiques détaillées pour un contenu spécifique."""
    try:
        date_debut, date_fin = _extraire_filtres_date()
        donnees = calculer_statistiques_contenu(id_contenu, date_debut, date_fin)
        if donnees:
            return jsonify({'succes': True, 'donnees': donnees})
        return jsonify({'succes': False, 'erreur': 'Contenu non trouvé'}), 404
    except Exception as exc:
        journal.error("Erreur stats contenu %s : %s", id_contenu, exc)
        return jsonify({'succes': False, 'erreur': 'Erreur interne du serveur'}), 500


@statistiques_bp.route('/api/statistiques/sessions')
def stats_sessions():
    """Retourne un résumé des sessions."""
    try:
        date_debut, date_fin = _extraire_filtres_date()
        donnees = calculer_resume_sessions(date_debut, date_fin)
        return jsonify({'succes': True, 'donnees': donnees})
    except Exception as exc:
        journal.error("Erreur stats sessions : %s", exc)
        return jsonify({'succes': False, 'erreur': 'Erreur interne du serveur'}), 500


@statistiques_bp.route('/api/statistiques/appareils')
def stats_appareils():
    """Retourne la répartition par type d'appareil."""
    try:
        date_debut, date_fin = _extraire_filtres_date()
        donnees = calculer_repartition_appareils(date_debut, date_fin)
        return jsonify({'succes': True, 'donnees': donnees})
    except Exception as exc:
        journal.error("Erreur stats appareils : %s", exc)
        return jsonify({'succes': False, 'erreur': 'Erreur interne du serveur'}), 500


@statistiques_bp.route('/api/statistiques/navigateurs')
def stats_navigateurs():
    """Retourne la répartition par navigateur."""
    try:
        date_debut, date_fin = _extraire_filtres_date()
        donnees = calculer_repartition_navigateurs(date_debut, date_fin)
        return jsonify({'succes': True, 'donnees': donnees})
    except Exception as exc:
        journal.error("Erreur stats navigateurs : %s", exc)
        return jsonify({'succes': False, 'erreur': 'Erreur interne du serveur'}), 500
