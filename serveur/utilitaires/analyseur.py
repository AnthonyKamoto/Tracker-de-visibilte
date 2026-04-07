"""
Fonctions de calcul statistique sur les données de visibilité.
"""

import re

from serveur.base_de_donnees import obtenir_connexion

# Format attendu : AAAA-MM-JJ
_FORMAT_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def _clause_date(date_debut=None, date_fin=None, colonne="e.date_enregistrement"):
    """Construit la clause WHERE pour filtrer par date."""
    conditions = []
    parametres = []
    if date_debut:
        if not _FORMAT_DATE.match(date_debut):
            return conditions, parametres
        conditions.append(f"{colonne} >= ?")
        parametres.append(date_debut)
    if date_fin:
        if not _FORMAT_DATE.match(date_fin):
            return conditions, parametres
        conditions.append(f"{colonne} <= ?")
        parametres.append(date_fin + " 23:59:59")
    return conditions, parametres


def calculer_statistiques_contenus(date_debut=None, date_fin=None):
    """Retourne les statistiques agrégées pour tous les contenus."""
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()

        conditions, parametres = _clause_date(date_debut, date_fin)
        clause_where = ""
        if conditions:
            clause_where = "WHERE " + " AND ".join(conditions)

        curseur.execute(f"""
            SELECT
                e.id_contenu,
                e.type_contenu,
                COUNT(*) AS nombre_vues,
                ROUND(AVG(e.duree_exposition_ms), 0) AS duree_moyenne_ms,
                ROUND(AVG(e.pourcentage_visibilite), 2) AS visibilite_moyenne
            FROM evenements_visibilite e
            {clause_where}
            GROUP BY e.id_contenu, e.type_contenu
            ORDER BY nombre_vues DESC
        """, parametres)

        return [dict(ligne) for ligne in curseur.fetchall()]
    finally:
        connexion.close()


def calculer_statistiques_contenu(id_contenu, date_debut=None, date_fin=None):
    """Retourne les statistiques détaillées pour un contenu spécifique."""
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()

        conditions, parametres = _clause_date(date_debut, date_fin)
        conditions.append("e.id_contenu = ?")
        parametres.append(id_contenu)
        clause_where = "WHERE " + " AND ".join(conditions)

        curseur.execute(f"""
            SELECT
                e.id_contenu,
                e.type_contenu,
                COUNT(*) AS nombre_vues,
                ROUND(AVG(e.duree_exposition_ms), 0) AS duree_moyenne_ms,
                ROUND(AVG(e.pourcentage_visibilite), 2) AS visibilite_moyenne,
                MIN(e.date_enregistrement) AS premiere_vue,
                MAX(e.date_enregistrement) AS derniere_vue
            FROM evenements_visibilite e
            {clause_where}
            GROUP BY e.id_contenu, e.type_contenu
        """, parametres)

        ligne = curseur.fetchone()
        if ligne:
            return dict(ligne)
        return None
    finally:
        connexion.close()


def calculer_resume_sessions(date_debut=None, date_fin=None):
    """Retourne un résumé des sessions."""
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()

        conditions_sessions, parametres_sessions = _clause_date(
            date_debut, date_fin, colonne="s.date_debut"
        )
        clause_where = ""
        if conditions_sessions:
            clause_where = "WHERE " + " AND ".join(conditions_sessions)

        curseur.execute(f"""
            SELECT
                COUNT(*) AS nombre_sessions,
                COUNT(DISTINCT s.type_appareil) AS types_appareils_distincts
            FROM sessions s
            {clause_where}
        """, parametres_sessions)

        resultat = dict(curseur.fetchone())

        # Nombre total d'événements
        conditions_evt, params_evt = _clause_date(date_debut, date_fin)
        clause_evt = ""
        if conditions_evt:
            clause_evt = "WHERE " + " AND ".join(conditions_evt)

        curseur.execute(f"""
            SELECT COUNT(*) AS nombre_evenements,
                   ROUND(AVG(e.duree_exposition_ms), 0) AS duree_moyenne_globale_ms,
                   ROUND(AVG(e.pourcentage_visibilite), 2) AS visibilite_moyenne_globale
            FROM evenements_visibilite e
            {clause_evt}
        """, params_evt)

        stats_evt = dict(curseur.fetchone())
        resultat.update(stats_evt)
        return resultat
    finally:
        connexion.close()


def calculer_repartition_appareils(date_debut=None, date_fin=None):
    """Retourne la répartition des sessions par type d'appareil."""
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()

        conditions, parametres = _clause_date(
            date_debut, date_fin, colonne="s.date_debut"
        )
        clause_where = ""
        if conditions:
            clause_where = "WHERE " + " AND ".join(conditions)

        curseur.execute(f"""
            SELECT s.type_appareil, COUNT(*) AS nombre
            FROM sessions s
            {clause_where}
            GROUP BY s.type_appareil
            ORDER BY nombre DESC
        """, parametres)

        return [dict(ligne) for ligne in curseur.fetchall()]
    finally:
        connexion.close()


def calculer_repartition_navigateurs(date_debut=None, date_fin=None):
    """Retourne la répartition des sessions par navigateur."""
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()

        conditions, parametres = _clause_date(
            date_debut, date_fin, colonne="s.date_debut"
        )
        clause_where = ""
        if conditions:
            clause_where = "WHERE " + " AND ".join(conditions)

        curseur.execute(f"""
            SELECT s.navigateur, COUNT(*) AS nombre
            FROM sessions s
            {clause_where}
            GROUP BY s.navigateur
            ORDER BY nombre DESC
        """, parametres)

        return [dict(ligne) for ligne in curseur.fetchall()]
    finally:
        connexion.close()
