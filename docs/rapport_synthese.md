# Rapport de synthese

Tracker de visibilite - Fondation CCC
Auteur : Anthony Kamoto
Annee : 2026

---

## Probleme traite

Sur le Web, un contenu affiche sur une page n'est pas necessairement vu par l'utilisateur. Les bannieres, images, textes et videos peuvent se trouver hors du champ de vision (en dessous de la ligne de flottaison, hors ecran apres un scroll rapide, etc.). Les outils d'analyse classiques (nombre de pages vues, clics) ne mesurent pas la **visibilite reelle** des contenus.

Ce projet propose un systeme capable de :

- Detecter si un contenu est effectivement visible dans la zone d'affichage du navigateur
- Mesurer le pourcentage de surface visible
- Calculer la duree d'exposition de chaque contenu
- Collecter des informations contextuelles (appareil, navigateur, resolution)
- Restituer ces donnees sous forme de statistiques et graphiques

---

## Architecture du systeme

Le systeme repose sur une architecture en trois couches :

```
 Navigateur (Front-end)          Serveur (Back-end)           Stockage
+---------------------+       +---------------------+     +-------------+
| IntersectionObserver |  -->  | Flask (API REST)    | --> | SQLite      |
| collecteur_donnees.js|  HTTP | routes/collecte.py  |     | visibilite.db|
| informations_contexte|       | routes/statistiques |     |             |
+---------------------+       +---------------------+     +-------------+
                                | CORS active         |
                                +---------------------+
                                       ^
                                       | HTTP GET (CORS)
                                       |
                               +---------------------+
                               | Dashboard (port 5001)|
                               | Chart.js             |
                               | Auto-refresh         |
                               +---------------------+
```

### Front-end (JavaScript)

- **observateur_visibilite.js** : utilise l'API IntersectionObserver pour detecter la visibilite de chaque element surveille et mesurer le pourcentage de surface visible.
- **collecteur_donnees.js** : agrege les evenements de visibilite et les envoie periodiquement au serveur via des requetes POST.
- **informations_contexte.js** : detecte le type d'appareil, le navigateur, la resolution d'ecran et les transmet au serveur lors de la creation de la session.

### Back-end (Python / Flask) -- Port 5000

- **appli.py** : point d'entree de l'application Flask, enregistre les blueprints et active CORS.
- **routes/collecte.py** : endpoints `POST /api/sessions` et `POST /api/evenements` pour recevoir les donnees du front-end.
- **routes/statistiques.py** : endpoints `GET /api/statistiques/*` pour fournir les donnees au tableau de bord.
- **routes/pages.py** : sert le site d'actualites (`/actualites`).
- **utilitaires/analyseur.py** : fonctions de calcul de statistiques (moyennes, repartitions, resumes).
- **base_de_donnees.py** : initialisation et connexion a la base de donnees SQLite.

### Dashboard (Python / Flask) -- Port 5001

- **dashboard/appli.py** : application Flask independante qui sert le tableau de bord.
- **dashboard/static/js/tableau_de_bord.js** : recupere les statistiques via les API du serveur principal et les affiche sous forme de graphiques interactifs avec Chart.js. Inclut un indicateur de connexion et un mode de rafraichissement automatique.

### Stockage (SQLite)

- Fichier unique `donnees/visibilite.db` cree automatiquement.
- Deux tables : `sessions` et `evenements_visibilite` reliees par cle etrangere.
- Index sur `id_contenu` et `id_session` pour accelerer les requetes.

---

## Technologies utilisees

| Composant        | Technologie              | Role                                              |
|------------------|--------------------------|---------------------------------------------------|
| Langage serveur  | Python 3.10+             | Logique metier et API                              |
| Framework web    | Flask + Flask-CORS         | Serveur HTTP, routage REST et gestion CORS         |
| Base de donnees  | SQLite                   | Stockage leger des sessions et evenements          |
| Detection visibilite | IntersectionObserver (API Web) | Detection de la visibilite dans le viewport   |
| Graphiques       | Chart.js                 | Visualisation des statistiques dans le dashboard   |
| Templates        | Jinja2 (via Flask)       | Rendu des pages HTML                               |
| Tests            | pytest                   | Framework de tests unitaires                       |
| Environnement    | venv                     | Environnement virtuel Python (isolement des dependances) |

> Le projet est compatible **Windows**, **macOS** et **Linux**. Toutes les dependances sont multiplateformes et le code utilise `os.path` pour la gestion des chemins de fichiers.

---

## Resultats obtenus

Le prototype est **fonctionnel au niveau 2** (application complete avec interface utilisateur, API REST et base de donnees).

### Fonctionnalites implementees

- **21 contenus surveilles** sur le site d'actualites : bannieres, articles, images, video, widgets, FAQ, newsletter et editoriaux avec des identifiants uniques.
- **Architecture separee** : le site d'actualites (port 5000) et le dashboard (port 5001) fonctionnent comme deux applications Flask independantes communiquant via API REST et CORS.
- **Collecte en temps reel** : les evenements de visibilite sont detectes et envoyes au serveur au fur et a mesure du scroll.
- **5 graphiques** sur le tableau de bord :
  1. Visibilite moyenne par contenu
  2. Duree d'exposition moyenne par contenu
  3. Repartition par type d'appareil
  4. Repartition par navigateur
  5. Nombre de vues par contenu
- **Filtre par plage de dates** : le tableau de bord permet de filtrer les donnees affichees selon une periode.
- **Rafraichissement automatique** : le dashboard dispose d'un toggle pour actualiser les donnees toutes les 10 secondes.
- **Indicateur de connexion** : le dashboard affiche l'etat de connexion au serveur principal en temps reel.
- **42 tests unitaires** : couverture des 5 modules principaux (base de donnees, collecte, statistiques, analyseur, dashboard), tous passent avec succes.
- **API REST complete** : 7 endpoints couvrant la collecte et la restitution des donnees.
- **Multiplateforme** : le projet fonctionne sur Windows, macOS et Linux. Des scripts de lancement (`lancer.ps1`, `lancer.sh`) permettent de demarrer les deux serveurs en une commande.

---

## Conclusion

Ce projet demontre la faisabilite d'un systeme de mesure de visibilite de contenus Web, du front-end au stockage en base de donnees, avec restitution graphique. Le prototype couvre l'ensemble du flux de donnees : detection par IntersectionObserver, collecte via API REST, stockage SQLite et affichage sur un tableau de bord interactif independant. L'architecture separee (site + dashboard) illustre une conception modulaire proche des pratiques professionnelles. Les 42 tests unitaires garantissent la fiabilite des composants principaux.
