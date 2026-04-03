"""
Routes API pour la collecte des données de visibilité.
"""

from flask import Blueprint, request, jsonify
from serveur.modeles.session import creer_session, obtenir_session
from serveur.modeles.evenement import enregistrer_lot_evenements

collecte_bp = Blueprint('collecte', __name__)


@collecte_bp.route('/api/sessions', methods=['POST'])
def creer_nouvelle_session():
    """Crée une nouvelle session utilisateur."""
    donnees = request.get_json(silent=True)

    if not donnees:
        return jsonify({'succes': False, 'erreur': 'Données JSON requises'}), 400

    champs_requis = ['id_session', 'type_appareil']
    for champ in champs_requis:
        if champ not in donnees:
            return jsonify({'succes': False, 'erreur': f'Champ requis manquant : {champ}'}), 400

    # Vérifier si la session existe déjà
    if obtenir_session(donnees['id_session']):
        return jsonify({'succes': True, 'id_session': donnees['id_session'], 'message': 'Session existante'}), 200

    try:
        id_session = creer_session(donnees)
        return jsonify({'succes': True, 'id_session': id_session}), 201
    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e)}), 500


@collecte_bp.route('/api/evenements', methods=['POST'])
def enregistrer_evenements():
    """Enregistre un lot d'événements de visibilité."""
    donnees = request.get_json(silent=True)

    # Gérer aussi les données envoyées via sendBeacon (Content-Type peut être text/plain)
    if not donnees:
        try:
            import json
            donnees = json.loads(request.get_data(as_text=True))
        except Exception:
            return jsonify({'succes': False, 'erreur': 'Données JSON requises'}), 400

    if 'id_session' not in donnees:
        return jsonify({'succes': False, 'erreur': 'Champ requis manquant : id_session'}), 400

    evenements = donnees.get('evenements', [])
    if not evenements:
        return jsonify({'succes': False, 'erreur': 'Aucun événement fourni'}), 400

    try:
        ids = enregistrer_lot_evenements(donnees['id_session'], evenements)
        return jsonify({
            'succes': True,
            'nombre_enregistres': len(ids)
        }), 201
    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e)}), 500
