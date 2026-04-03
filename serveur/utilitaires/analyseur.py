"""
Fonctions de calcul statistique sur les données de visibilité.
"""

from serveur.base_de_donnees import obtenir_connexion


def _clause_date(date_debut=None, date_fin=None, prefixe="e"):
    """Construit la clause WHERE pour filtrer par date."""
    conditions = []
    parametres = []
    if date_debut:
        conditions.append(f"{prefixe}.date_enregistrement >= ?")
        parametres.append(date_debut)
    if date_fin:
        conditions.append(f"{prefixe}.date_enregistrement <= ?")
        parametres.append(date_fin + " 23:59:59")
    return conditions, parametres


def calculer_statistiques_contenus(date_debut=None, date_fin=None):
    """Retourne les statistiques agrégées pour tous les contenus."""
    connexion = obtenir_connexion()
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
        GROUP BY e.id_contenu
        ORDER BY nombre_vues DESC
    """, parametres)

    resultats = [dict(ligne) for ligne in curseur.fetchall()]
    connexion.close()
    return resultats


def calculer_statistiques_contenu(id_contenu, date_debut=None, date_fin=None):
    """Retourne les statistiques détaillées pour un contenu spécifique."""
    connexion = obtenir_connexion()
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
        GROUP BY e.id_contenu
    """, parametres)

    ligne = curseur.fetchone()
    connexion.close()
    if ligne:
        return dict(ligne)
    return None


def calculer_resume_sessions(date_debut=None, date_fin=None):
    """Retourne un résumé des sessions."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()

    conditions, parametres = _clause_date(date_debut, date_fin, prefixe="s")
    # Adapter le filtre de date pour la table sessions
    conditions_sessions = [c.replace("s.date_enregistrement", "s.date_debut") for c in conditions]
    clause_where = ""
    if conditions_sessions:
        clause_where = "WHERE " + " AND ".join(conditions_sessions)

    curseur.execute(f"""
        SELECT
            COUNT(*) AS nombre_sessions,
            COUNT(DISTINCT s.type_appareil) AS types_appareils_distincts
        FROM sessions s
        {clause_where}
    """, parametres)

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
    connexion.close()
    return resultat


def calculer_repartition_appareils(date_debut=None, date_fin=None):
    """Retourne la répartition des sessions par type d'appareil."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()

    conditions, parametres = _clause_date(date_debut, date_fin, prefixe="s")
    conditions = [c.replace("s.date_enregistrement", "s.date_debut") for c in conditions]
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

    resultats = [dict(ligne) for ligne in curseur.fetchall()]
    connexion.close()
    return resultats


def calculer_repartition_navigateurs(date_debut=None, date_fin=None):
    """Retourne la répartition des sessions par navigateur."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor()

    conditions, parametres = _clause_date(date_debut, date_fin, prefixe="s")
    conditions = [c.replace("s.date_enregistrement", "s.date_debut") for c in conditions]
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

    resultats = [dict(ligne) for ligne in curseur.fetchall()]
    connexion.close()
    return resultats
