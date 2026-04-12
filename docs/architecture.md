# Architecture du Tracker de visibilite -- Fondation CCC

## 1. Vue d'ensemble

Le systeme de mesure de visibilite web de la Fondation CCC est une application
quatre-couches concue pour detecter, collecter et analyser la visibilite des
contenus affiches dans le navigateur d'un visiteur.

Les quatre couches sont les suivantes :

| Couche | Role | Technologies |
|--------|------|--------------|
| **Front-end (navigateur)** | Detecte la visibilite des contenus via `IntersectionObserver`, collecte les informations contextuelles (appareil, navigateur, ecran) et envoie les evenements par lots au serveur. | HTML5, CSS3, JavaScript vanilla, IntersectionObserver API, Chart.js |
| **Back-end (serveur Flask)** | Expose une API REST pour recevoir les sessions et les evenements, sert le site d'actualites et fournit les routes de statistiques. Active CORS pour permettre la communication avec le dashboard. | Python 3.10+, Flask 3.x, Flask-CORS |
| **Dashboard (application separee)** | Application Flask independante qui consomme les API de statistiques du serveur principal et affiche les resultats dans des graphiques interactifs. | Python 3.10+, Flask 3.x, Chart.js |
| **Base de donnees (SQLite)** | Stocke les sessions utilisateur et les evenements de visibilite dans un fichier local (`donnees/visibilite.db`). | SQLite 3 |

---

## 2. Schema d'architecture

```
+---------------------------------------------------------------+
|                      NAVIGATEUR (client)                      |
|                                                               |
|  +-------------------------+   +--------------------------+   |
|  | InformationsContexte    |   | ObservateurVisibilite    |   |
|  | - type_appareil         |   | - IntersectionObserver   |   |
|  | - navigateur            |   | - seuils : 0/25/50/75/100|  |
|  | - taille ecran          |   | - heartbeat (5 s)        |   |
|  | - page consultee        |   | - evenements visibilite  |   |
|  +------------+------------+   +------------+-------------+   |
|               |                             |                 |
|               v                             v                 |
|          +----+-----------------------------+------+          |
|          |       CollecteurDonnees                 |          |
|          | - tampon (max 5 evenements)              |          |
|          | - envoi periodique (3 s)                 |          |
|          | - fetch() / sendBeacon()                 |          |
|          +--------------------+--------------------+          |
+-------------------------------|-------------------------------+
                                |
                     HTTP POST (JSON)
                                |
                                v
+-------------------------------|-------------------------------+
|              SERVEUR D'ACTUALITES (port 5000)                 |
|                                                               |
|  +--------------------+   +-----------------------------+     |
|  | Routes pages       |   | Routes collecte (API)       |     |
|  | GET /              |   | POST /api/sessions          |     |
|  | GET /actualites    |   | POST /api/evenements        |     |
|  +--------------------+   +-----------------------------+     |
|                                                               |
|  +--------------------+   +-----------------------------+     |
|  | Modeles            |   | Routes statistiques (API)   |     |
|  | - session.py       |   | GET /api/statistiques/      |     |
|  | - evenement.py     |   |     contenus                |     |
|  +--------------------+   |     contenus/<id>           |     |
|                           |     sessions                |     |
|  +--------------------+   |     appareils               |     |
|  | Utilitaires        |   |     navigateurs             |     |
|  | - analyseur.py     |   +-----------------------------+     |
|  +--------------------+                                       |
|                           +-----------------------------+     |
|                           | Routes exportation (API)    |     |
|                           | GET /api/exportation/xlsx   |     |
|                           | GET /api/exportation/csv    |     |
|                           +-----------------------------+     |
|                                  CORS active                  |
+-------------------------------|-------------------------------+
                                |
              Lecture / Ecriture |         HTTP GET (JSON + CORS)
                                |                |
                                v                |
+-------------------------------+                |
|      BASE DE DONNEES SQLite   |                |
|   donnees/visibilite.db       |                |
|                               |                |
|  +----------+ +------------+ |                |
|  | sessions | | evenements | |                |
|  +----------+ +------------+ |                |
+-------------------------------+                |
                                                 v
                          +------------------------------+
                          |   DASHBOARD (port 5001)      |
                          |                              |
                          | - Application Flask separee  |
                          | - Appelle les API du serveur |
                          | - Affiche les graphiques     |
                          |   (Chart.js)                 |
                          | - Rafraichissement auto      |
                          | - Indicateur de connexion    |
                          | - Export des donnees (XLSX,  |
                          |   CSV) via l'API serveur     |
                          +------------------------------+
```

---

## 3. Flux de donnees

Voici le parcours complet d'un evenement de visibilite, de la detection dans le
navigateur jusqu'a l'affichage dans le tableau de bord.

### 3.1 Detection (navigateur)

1. **Chargement de la page** -- Au chargement du DOM, trois modules JavaScript
   s'initialisent :
   - `InformationsContexte` collecte les donnees de l'appareil (type, taille
     d'ecran, navigateur, URL).
   - `CollecteurDonnees` genere un identifiant de session (UUID v4) et envoie
     une requete `POST /api/sessions` pour l'enregistrer cote serveur.
   - `ObservateurVisibilite` cree une instance d'`IntersectionObserver` avec les
     seuils `[0, 0.25, 0.5, 0.75, 1.0]` et observe chaque element HTML portant
     l'attribut `data-contenu-id`.

2. **Observation** -- Lorsqu'un contenu franchit un seuil de visibilite,
   l'observateur enregistre :
   - l'identifiant et le type du contenu,
   - le pourcentage de visibilite,
   - l'horodatage de debut et de fin d'exposition,
   - la duree d'exposition en millisecondes.

3. **Mise en tampon** -- L'evenement est ajoute au tampon du
   `CollecteurDonnees`. Un heartbeat toutes les 5 secondes capture l'etat des
   contenus encore visibles (pour eviter toute perte en cas de fermeture soudaine).

### 3.2 Transmission (navigateur vers serveur)

4. **Envoi par lots** -- Le tampon est vide automatiquement selon deux
   mecanismes :
   - **Seuil de taille** : des que le tampon atteint 5 evenements, un envoi
     `fetch POST /api/evenements` est declenche.
   - **Intervalle** : toutes les 3 secondes, le tampon est envoye meme s'il
     contient moins de 5 evenements.

5. **Fermeture de page** -- A l'evenement `beforeunload` ou lorsque l'onglet
   devient masque (`visibilitychange`), les evenements restants sont envoyes via
   `navigator.sendBeacon()` pour garantir la livraison meme si la page se ferme.

### 3.3 Enregistrement (serveur)

6. **Reception** -- La route `POST /api/evenements` du blueprint `collecte`
   recoit le lot JSON. Le serveur accepte aussi les donnees envoyees par
   `sendBeacon` (qui peut emettre avec un `Content-Type` different).

7. **Insertion en base** -- Le modele `evenement.py` insere le lot d'evenements
   dans la table `evenements_visibilite` en une seule transaction SQLite. Chaque
   evenement est associe a la session via la cle etrangere `id_session`.

### 3.4 Consultation (tableau de bord)

8. **Requete des statistiques** -- Le dashboard (application separee sur le
   port 5001) charge les donnees en appelant simultanement quatre endpoints
   du serveur principal (port 5000) via CORS :
   - `GET /api/statistiques/contenus` -- statistiques agregees par contenu
   - `GET /api/statistiques/sessions` -- resume global (nombre de sessions,
     visibilite moyenne, duree moyenne)
   - `GET /api/statistiques/appareils` -- repartition par type d'appareil
   - `GET /api/statistiques/navigateurs` -- repartition par navigateur

9. **Calcul** -- Le module `analyseur.py` execute des requetes SQL d'agregation
   (`AVG`, `COUNT`, `GROUP BY`) sur la base SQLite et retourne les resultats
   au format JSON. Les filtres optionnels `date_debut` et `date_fin` permettent
   de restreindre la periode analysee.

10. **Affichage** -- Le script `tableau_de_bord.js` recoit les donnees JSON et
    genere les graphiques via Chart.js : barres horizontales (visibilite
    moyenne), barres verticales (duree moyenne, nombre de vues), donut (appareils)
    et camembert (navigateurs). Un tableau HTML recapitulatif est egalement
    rempli dynamiquement.

### 3.5 Exportation (dashboard vers fichier)

11. **Export des donnees** -- Le dashboard propose deux boutons d'exportation
    (Excel et CSV). Les boutons declenchent un telechargement via les endpoints
    `GET /api/exportation/xlsx` et `GET /api/exportation/csv` du serveur
    principal. Le serveur construit un tableau croise unique (une ligne par
    contenu, avec colonnes dynamiques par type d'appareil et par navigateur)
    en joignant les tables `evenements_visibilite` et `sessions`. Les fichiers
    sont sauvegardes dans le dossier `exports/` (ecrases a chaque export) et
    retournes en telechargement. Les filtres de date du dashboard s'appliquent.

---

## 4. Technologies utilisees

### Front-end

| Technologie | Utilisation |
|-------------|-------------|
| **HTML5** | Structure des pages (demo et tableau de bord), attributs `data-contenu-id` pour le marquage des contenus |
| **CSS3** | Mise en forme des pages (`style_demo.css`, `style_tableau_de_bord.css`), Google Fonts (Playfair Display, Inter), Font Awesome |
| **JavaScript vanilla** | Logique de detection, collecte, envoi des donnees et rendu du tableau de bord -- aucun framework |
| **IntersectionObserver API** | Detection native de la visibilite des elements dans le viewport avec seuils multiples |
| **Chart.js** | Generation des graphiques interactifs dans le tableau de bord (barres, donut, camembert) |

### Back-end

| Technologie | Utilisation |
|-------------|-------------|
| **Python 3.10+** | Langage du serveur |
| **Flask 3.x** | Framework web -- routage, blueprints, JSON, templates Jinja2 |
| **Flask-CORS** | Gestion des requetes cross-origin (CORS) pour la communication entre le site et le dashboard |
| **openpyxl** | Generation de fichiers Excel (XLSX) pour l'export des statistiques |

### Base de donnees

| Technologie | Utilisation |
|-------------|-------------|
| **SQLite 3** | Stockage local des sessions et des evenements dans `donnees/visibilite.db`, clefs etrangeres activees, index sur `id_contenu` et `id_session` |

### Tests

| Technologie | Utilisation |
|-------------|-------------|
| **pytest** | Tests unitaires et d'integration couvrant la base de donnees, les routes de collecte, les routes de statistiques, les routes d'exportation et le module d'analyse |

---

## 5. Types de contenu

### 5.1 Types de contenu supportes

Le systeme de tracking supporte les types de contenu suivants (extensibles) :

| Type | Description |
|------|-------------|
| **banniere** | Bannière publicitaire, promotionnelle ou informationnelle |
| **texte** | Bloc de texte, paragraphes, articles, sections informatives |
| **image** | Images, cartes, illustrations, photo produit |
| **video** | Vidéo embarquée, iframes YouTube/Vimeo, conteneur vidéo |
| **widget** | Petit bloc informatif : statistiques, miniatures, compteurs |
| **galerie** | Groupement d'images (carrousel, grille) |
| **cta** | Call-To-Action, boutons, sections engageantes |
| **faq** | Section FAQ, bloc de questions-réponses |
| **faq-item** | Élément individuel de FAQ (question + réponse collapsible) |

Les éléments HTML doivent porter les attributs `data-contenu-id` (identifiant unique) et `data-type-contenu` (type) pour être automatiquement tracés par l'`IntersectionObserver`.

---

## 6. Structure des dossiers

```
📁 Projet_N4_CCC_Anthony_Kamoto/
|
|-- 📁 serveur/                        # Serveur principal (port 5000)
|   |-- 🐍 __init__.py
|   |-- 🐍 appli.py                    # Point d'entree Flask + CORS
|   |-- 🐍 config.py                   # Configuration (hote, port, chemin BDD)
|   |-- 🐍 base_de_donnees.py          # Connexion SQLite et creation des tables
|   |
|   |-- 📁 modeles/                    # Couche d'acces aux donnees
|   |   |-- 🐍 __init__.py
|   |   |-- 🐍 session.py              # CRUD sessions
|   |   |-- 🐍 evenement.py            # CRUD evenements de visibilite
|   |
|   |-- 📁 routes/                     # Blueprints Flask (API + pages)
|   |   |-- 🐍 __init__.py
|   |   |-- 🐍 pages.py                # Routes HTML : /, /actualites
|   |   |-- 🐍 collecte.py             # API collecte : /api/sessions, /api/evenements
|   |   |-- 🐍 statistiques.py         # API stats : /api/statistiques/*
|   |   |-- 🐍 exportation.py          # API export : /api/exportation/xlsx, /api/exportation/csv
|   |
|   |-- 📁 utilitaires/                # Fonctions transversales
|       |-- 🐍 __init__.py
|       |-- 🐍 analyseur.py            # Calculs statistiques (agregations SQL)
|
|-- 📁 dashboard/                      # Dashboard independant (port 5001)
|   |-- 🐍 __init__.py
|   |-- 🐍 appli.py                    # Point d'entree Flask du dashboard
|   |-- 🐍 config.py                   # Configuration (port, URL serveur)
|   |-- 📁 templates/
|   |   |-- 🌐 tableau_de_bord.html    # Page du tableau de bord
|   |-- 📁 static/
|       |-- 📁 css/
|       |   |-- 🎨 style_tableau_de_bord.css  # Styles du dashboard
|       |-- 📁 js/
|           |-- ⚡ tableau_de_bord.js          # Graphiques Chart.js + auto-refresh
|
|-- 📁 templates/                       # Templates HTML du site d'actualites
|   |-- 🌐 actualites.html              # Site d'actualites (21 elements surveilles)
|
|-- 📁 static/                          # Fichiers statiques du site d'actualites
|   |-- 📁 css/
|   |   |-- 🎨 style_demo.css          # Styles du site d'actualites
|   |
|   |-- 📁 js/
|       |-- ⚡ informations_contexte.js   # Detection appareil/navigateur/ecran
|       |-- ⚡ observateur_visibilite.js  # Observation via IntersectionObserver
|       |-- ⚡ collecteur_donnees.js      # Tampon, envoi par lots, sendBeacon
|
|-- 📁 donnees/                        # Base de donnees SQLite (generee au lancement)
|   |-- 🗄️ visibilite.db
|
|-- 📁 exports/                        # Fichiers d'export generes (XLSX, CSV, non suivis par git)
|
|-- 📁 tests/                          # Tests automatises (pytest)
|   |-- 🐍 conftest.py                 # Configuration partagee des tests
|   |-- 🐍 test_base_de_donnees.py     # Tests de la couche base de donnees
|   |-- 🐍 test_routes_collecte.py     # Tests des routes de collecte
|   |-- 🐍 test_routes_statistiques.py # Tests des routes de statistiques
|   |-- 🐍 test_routes_exportation.py  # Tests des routes d'exportation
|   |-- 🐍 test_analyseur.py           # Tests du module d'analyse
|   |-- 🐍 test_dashboard.py           # Tests du dashboard
|
|-- 📁 docs/                           # Documentation du projet
|   |-- 📝 architecture.md             # Ce fichier
|   |-- 📝 base_de_donnees.md          # Schema de la BDD
|   |-- 📝 guide_installation.md       # Guide d'installation
|   |-- 📝 rapport_synthese.md         # Rapport de synthese
|
|-- 🪟 lancer.ps1                      # Script de lancement (Windows)
|-- 🐧 lancer.sh                       # Script de lancement (macOS/Linux)
|-- 📋 requirements.txt                # Dependances Python (flask, flask-cors, pytest, openpyxl)
```
