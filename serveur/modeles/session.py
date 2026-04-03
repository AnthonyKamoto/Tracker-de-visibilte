"""
Modèle de données pour les sessions utilisateur.
"""

from serveur.base_de_donnees import obtenir_connexion


def creer_session(donnees):
    """Insère une nouvelle session dans la base de données."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO sessions (id_session, type_appareil, largeur_ecran,
                              hauteur_ecran, navigateur, page_consultee)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        donnees['id_session'],
        donnees['type_appareil'],
        donnees.get('largeur_ecran'),
        donnees.get('hauteur_ecran'),
        donnees.get('navigateur'),
        donnees.get('page_consultee')
    ))
    connexion.commit()
    connexion.close()
    return donnees['id_session']


def obtenir_session(id_session):
    """Récupère une session par son identifiant."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM sessions WHERE id_session = ?", (id_session,))
    session = curseur.fetchone()
    connexion.close()
    if session:
        return dict(session)
    return None
