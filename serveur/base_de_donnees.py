"""
Initialisation et gestion de la base de données SQLite.
"""

import sqlite3
import os
from serveur.config import CHEMIN_BDD, DELAI_ATTENTE_BDD


def obtenir_connexion():
    """Retourne une connexion à la base de données SQLite."""
    repertoire = os.path.dirname(CHEMIN_BDD)
    if not os.path.exists(repertoire):
        os.makedirs(repertoire)

    connexion = sqlite3.connect(CHEMIN_BDD, timeout=DELAI_ATTENTE_BDD)
    connexion.row_factory = sqlite3.Row
    connexion.execute("PRAGMA foreign_keys = ON")
    connexion.execute("PRAGMA journal_mode = WAL")
    return connexion


def initialiser_bdd():
    """Crée les tables si elles n'existent pas encore."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id_session TEXT PRIMARY KEY,
            type_appareil TEXT NOT NULL,
            largeur_ecran INTEGER,
            hauteur_ecran INTEGER,
            navigateur TEXT,
            page_consultee TEXT,
            date_debut TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS evenements_visibilite (
            id_evenement INTEGER PRIMARY KEY AUTOINCREMENT,
            id_session TEXT NOT NULL,
            id_contenu TEXT NOT NULL,
            type_contenu TEXT,
            pourcentage_visibilite REAL NOT NULL,
            duree_exposition_ms INTEGER DEFAULT 0,
            horodatage_debut TEXT,
            horodatage_fin TEXT,
            date_enregistrement TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (id_session) REFERENCES sessions(id_session)
        )
    """)

    # Types de contenu acceptés :
    # - banniere : bannière publicitaire ou promotionnelle
    # - texte : bloc de texte, paragraphes, articles
    # - image : images, cartes, illustrations
    # - video : vidéo embarquée, iframes YouTube/Vimeo
    # - widget : petit bloc informatif (statistiques, miniatures)
    # - galerie : groupement d'images
    # - cta : call-to-action, boutons, sections engageantes
    # - faq : section de FAQ
    # - faq-item : élément individuel de FAQ

    curseur.execute("""
        CREATE INDEX IF NOT EXISTS idx_evenements_contenu
        ON evenements_visibilite(id_contenu)
    """)
    curseur.execute("""
        CREATE INDEX IF NOT EXISTS idx_evenements_session
        ON evenements_visibilite(id_session)
    """)
    curseur.execute("""
        CREATE INDEX IF NOT EXISTS idx_evenements_date
        ON evenements_visibilite(date_enregistrement)
    """)
    curseur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sessions_date
        ON sessions(date_debut)
    """)

    connexion.commit()
    connexion.close()
