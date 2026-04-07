"""
Modèle de données pour les événements de visibilité.
"""

from serveur.base_de_donnees import obtenir_connexion


def enregistrer_lot_evenements(id_session, evenements):
    """Insère un lot d'événements de visibilité en une seule transaction."""
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()
        donnees_lot = [
            (
                id_session,
                evt['id_contenu'],
                evt.get('type_contenu'),
                evt['pourcentage_visibilite'],
                evt.get('duree_exposition_ms', 0),
                evt.get('horodatage_debut'),
                evt.get('horodatage_fin')
            )
            for evt in evenements
        ]
        curseur.executemany("""
            INSERT INTO evenements_visibilite
                (id_session, id_contenu, type_contenu, pourcentage_visibilite,
                 duree_exposition_ms, horodatage_debut, horodatage_fin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, donnees_lot)
        connexion.commit()
        return len(donnees_lot)
    finally:
        connexion.close()
