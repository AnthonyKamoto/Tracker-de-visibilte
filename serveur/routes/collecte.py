"""
Routes API pour la collecte des données de visibilité.
"""

import json
import logging

from flask import Blueprint, request, jsonify
from serveur.modeles.session import creer_session, obtenir_session
from serveur.modeles.evenement import enregistrer_lot_evenements

collecte_bp = Blueprint('collecte', __name__)
journal = logging.getLogger(__name__)

# Limites de validation
TAILLE_MAX_CHAINE = 256
TAILLE_MAX_LOT = 500


def _valider_chaine(valeur, nom_champ, obligatoire=False):
    """Vérifie qu'une valeur est une chaîne valide et non vide si obligatoire."""
    if valeur is None:
        if obligatoire:
            return f"Champ requis manquant : {nom_champ}"
        return None
    if not isinstance(valeur, str) or len(valeur) > TAILLE_MAX_CHAINE:
        return f"Champ invalide : {nom_champ}"
    if obligatoire and len(valeur.strip()) == 0:
        return f"Champ requis manquant : {nom_champ}"
    return None


def _valider_entier(valeur, nom_champ):
    """Vérifie qu'une valeur est un entier positif (pas de flottant)."""
    if valeur is None:
        return None
    if isinstance(valeur, bool) or not isinstance(valeur, int) or valeur < 0:
        return f"Champ invalide : {nom_champ}"
    return None


@collecte_bp.route('/api/sessions', methods=['POST'])
def creer_nouvelle_session():
    """Crée une nouvelle session utilisateur."""
    donnees = request.get_json(silent=True)

    if not donnees:
        return jsonify({'succes': False, 'erreur': 'Données JSON requises'}), 400

    # Validation des champs
    erreur = _valider_chaine(donnees.get('id_session'), 'id_session', obligatoire=True)
    if erreur:
        return jsonify({'succes': False, 'erreur': erreur}), 400

    erreur = _valider_chaine(donnees.get('type_appareil'), 'type_appareil', obligatoire=True)
    if erreur:
        return jsonify({'succes': False, 'erreur': erreur}), 400

    erreur = _valider_entier(donnees.get('largeur_ecran'), 'largeur_ecran')
    if erreur:
        return jsonify({'succes': False, 'erreur': erreur}), 400

    erreur = _valider_entier(donnees.get('hauteur_ecran'), 'hauteur_ecran')
    if erreur:
        return jsonify({'succes': False, 'erreur': erreur}), 400

    erreur = _valider_chaine(donnees.get('navigateur'), 'navigateur')
    if erreur:
        return jsonify({'succes': False, 'erreur': erreur}), 400

    erreur = _valider_chaine(donnees.get('page_consultee'), 'page_consultee')
    if erreur:
        return jsonify({'succes': False, 'erreur': erreur}), 400

    # Vérifier si la session existe déjà
    if obtenir_session(donnees['id_session']):
        return jsonify({'succes': True, 'id_session': donnees['id_session'], 'message': 'Session existante'}), 200

    try:
        id_session = creer_session(donnees)
        return jsonify({'succes': True, 'id_session': id_session}), 201
    except Exception as exc:
        journal.error("Erreur creation session : %s", exc)
        return jsonify({'succes': False, 'erreur': 'Erreur lors de la création de la session'}), 500


@collecte_bp.route('/api/evenements', methods=['POST'])
def enregistrer_evenements():
    """Enregistre un lot d'événements de visibilité."""
    donnees = request.get_json(silent=True)

    # Gérer aussi les données envoyées via sendBeacon (Content-Type peut être text/plain)
    if not donnees:
        try:
            donnees = json.loads(request.get_data(as_text=True))
        except Exception:
            return jsonify({'succes': False, 'erreur': 'Données JSON requises'}), 400

    if 'id_session' not in donnees:
        return jsonify({'succes': False, 'erreur': 'Champ requis manquant : id_session'}), 400

    erreur = _valider_chaine(donnees.get('id_session'), 'id_session', obligatoire=True)
    if erreur:
        return jsonify({'succes': False, 'erreur': erreur}), 400

    evenements = donnees.get('evenements', [])
    if not evenements:
        return jsonify({'succes': False, 'erreur': 'Aucun événement fourni'}), 400

    if not isinstance(evenements, list) or len(evenements) > TAILLE_MAX_LOT:
        return jsonify({'succes': False, 'erreur': f'Le lot ne peut pas dépasser {TAILLE_MAX_LOT} événements'}), 400

    # Validation de chaque événement
    for evt in evenements:
        if not isinstance(evt, dict):
            return jsonify({'succes': False, 'erreur': 'Format d\'événement invalide'}), 400
        if 'id_contenu' not in evt or 'pourcentage_visibilite' not in evt:
            return jsonify({'succes': False, 'erreur': 'Champs requis : id_contenu, pourcentage_visibilite'}), 400
        erreur = _valider_chaine(evt.get('id_contenu'), 'id_contenu', obligatoire=True)
        if erreur:
            return jsonify({'succes': False, 'erreur': erreur}), 400
        erreur = _valider_chaine(evt.get('type_contenu'), 'type_contenu')
        if erreur:
            return jsonify({'succes': False, 'erreur': erreur}), 400
        pv = evt['pourcentage_visibilite']
        if isinstance(pv, bool) or not isinstance(pv, (int, float)) or pv < 0 or pv > 1:
            return jsonify({'succes': False, 'erreur': 'pourcentage_visibilite doit être entre 0 et 1'}), 400
        erreur = _valider_entier(evt.get('duree_exposition_ms'), 'duree_exposition_ms')
        if erreur:
            return jsonify({'succes': False, 'erreur': erreur}), 400
        erreur = _valider_chaine(evt.get('horodatage_debut'), 'horodatage_debut')
        if erreur:
            return jsonify({'succes': False, 'erreur': erreur}), 400
        erreur = _valider_chaine(evt.get('horodatage_fin'), 'horodatage_fin')
        if erreur:
            return jsonify({'succes': False, 'erreur': erreur}), 400

    # Vérifier que la session existe avant l'insertion (clé étrangère)
    if not obtenir_session(donnees['id_session']):
        return jsonify({'succes': False, 'erreur': 'Session introuvable'}), 404

    try:
        nombre = enregistrer_lot_evenements(donnees['id_session'], evenements)
        return jsonify({
            'succes': True,
            'nombre_enregistres': nombre
        }), 201
    except Exception as exc:
        journal.error("Erreur enregistrement evenements : %s", exc)
        return jsonify({'succes': False, 'erreur': 'Erreur lors de l\'enregistrement des événements'}), 500
