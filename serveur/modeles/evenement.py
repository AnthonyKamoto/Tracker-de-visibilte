"""
Modèle de données pour les événements de visibilité.
"""

from serveur.base_de_donnees import obtenir_connexion


def enregistrer_evenement(donnees):
    """Insère un événement de visibilité dans la base de données."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO evenements_visibilite
            (id_session, id_contenu, type_contenu, pourcentage_visibilite,
             duree_exposition_ms, horodatage_debut, horodatage_fin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        donnees['id_session'],
        donnees['id_contenu'],
        donnees.get('type_contenu'),
        donnees['pourcentage_visibilite'],
        donnees.get('duree_exposition_ms', 0),
        donnees.get('horodatage_debut'),
        donnees.get('horodatage_fin')
    ))
    connexion.commit()
    id_evenement = curseur.lastrowid
    connexion.close()
    return id_evenement


def enregistrer_lot_evenements(id_session, evenements):
    """Insère un lot d'événements de visibilité en une seule transaction."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    ids_inseres = []

    for evt in evenements:
        curseur.execute("""
            INSERT INTO evenements_visibilite
                (id_session, id_contenu, type_contenu, pourcentage_visibilite,
                 duree_exposition_ms, horodatage_debut, horodatage_fin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            id_session,
            evt['id_contenu'],
            evt.get('type_contenu'),
            evt['pourcentage_visibilite'],
            evt.get('duree_exposition_ms', 0),
            evt.get('horodatage_debut'),
            evt.get('horodatage_fin')
        ))
        ids_inseres.append(curseur.lastrowid)

    connexion.commit()
    connexion.close()
    return ids_inseres


def obtenir_evenements_par_contenu(id_contenu):
    """Récupère tous les événements pour un contenu donné."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT * FROM evenements_visibilite
        WHERE id_contenu = ?
        ORDER BY date_enregistrement DESC
    """, (id_contenu,))
    evenements = [dict(ligne) for ligne in curseur.fetchall()]
    connexion.close()
    return evenements
