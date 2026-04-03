# Architecture du systeme de mesure de visibilite web -- Fondation CCC

## 1. Vue d'ensemble

Le systeme de mesure de visibilite web de la Fondation CCC est une application
trois-couches concue pour detecter, collecter et analyser la visibilite des
contenus affiches dans le navigateur d'un visiteur.

Les trois couches sont les suivantes :

| Couche | Role | Technologies |
|--------|------|--------------|
| **Front-end (navigateur)** | Detecte la visibilite des contenus via `IntersectionObserver`, collecte les informations contextuelles (appareil, navigateur, ecran) et envoie les evenements par lots au serveur. | HTML5, CSS3, JavaScript vanilla, IntersectionObserver API, Chart.js |
| **Back-end (serveur Flask)** | Expose une API REST pour recevoir les sessions et les evenements, sert les pages HTML (demo et tableau de bord) et fournit les routes de statistiques. | Python 3.12, Flask 3.x |
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
|          | - tampon (max 10 evenements)             |          |
|          | - envoi periodique (5 s)                 |          |
|          | - fetch() / sendBeacon()                 |          |
|          +--------------------+--------------------+          |
+-------------------------------|-------------------------------+
                                |
                     HTTP POST (JSON)
                                |
                                v
+-------------------------------|-------------------------------+
|                   SERVEUR FLASK (back-end)                    |
|                                                               |
|  +--------------------+   +-----------------------------+     |
|  | Routes pages       |   | Routes collecte (API)       |     |
|  | GET /              |   | POST /api/sessions          |     |
|  | GET /demo          |   | POST /api/evenements        |     |
|  | GET /tableau-de-   |   +-----------------------------+     |
|  |      bord          |                                       |
|  +--------------------+   +-----------------------------+     |
|                           | Routes statistiques (API)   |     |
|  +--------------------+   | GET /api/statistiques/      |     |
|  | Modeles            |   |     contenus                |     |
|  | - session.py       |   |     contenus/<id>           |     |
|  | - evenement.py     |   |     sessions                |     |
|  +--------------------+   |     appareils               |     |
|                           |     navigateurs             |     |
|  +--------------------+   +-----------------------------+     |
|  | Utilitaires        |                                       |
|  | - analyseur.py     |                                       |
|  +--------------------+                                       |
+-------------------------------|-------------------------------+
                                |
                      Lecture / Ecriture
                                |
                                v
+-------------------------------|-------------------------------+
|                     BASE DE DONNEES SQLite                    |
|                  donnees/visibilite.db                        |
|                                                               |
|  +-------------------------+  +----------------------------+  |
|  | Table : sessions        |  | Table : evenements_        |  |
|  |-------------------------|  |          visibilite        |  |
|  | id_session (PK)         |  | id_evenement (PK, auto)   |  |
|  | type_appareil           |  | id_session (FK)            |  |
|  | largeur_ecran           |  | id_contenu                 |  |
|  | hauteur_ecran           |  | type_contenu               |  |
|  | navigateur              |  | pourcentage_visibilite     |  |
|  | page_consultee          |  | duree_exposition_ms        |  |
|  | date_debut              |  | horodatage_debut           |  |
|  +-------------------------+  | horodatage_fin             |  |
|                               | date_enregistrement        |  |
|                               +----------------------------+  |
+---------------------------------------------------------------+
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
   - **Seuil de taille** : des que le tampon atteint 10 evenements, un envoi
     `fetch POST /api/evenements` est declenche.
   - **Intervalle** : toutes les 5 secondes, le tampon est envoye meme s'il
     contient moins de 10 evenements.

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

8. **Requete des statistiques** -- Le tableau de bord (`/tableau-de-bord`)
   charge les donnees en appelant simultanement quatre endpoints :
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

---

## 4. Technologies utilisees

### Front-end

| Technologie | Utilisation |
|-------------|-------------|
| **HTML5** | Structure des pages (demo et tableau de bord), attributs `data-contenu-id` pour le marquage des contenus |
| **CSS3** | Mise en forme des pages (`style_demo.css`, `style_tableau_de_bord.css`) |
| **JavaScript vanilla** | Logique de detection, collecte, envoi des donnees et rendu du tableau de bord -- aucun framework |
| **IntersectionObserver API** | Detection native de la visibilite des elements dans le viewport avec seuils multiples |
| **Chart.js** | Generation des graphiques interactifs dans le tableau de bord (barres, donut, camembert) |

### Back-end

| Technologie | Utilisation |
|-------------|-------------|
| **Python 3.12** | Langage du serveur |
| **Flask 3.x** | Framework web -- routage, blueprints, JSON, templates Jinja2 |

### Base de donnees

| Technologie | Utilisation |
|-------------|-------------|
| **SQLite 3** | Stockage local des sessions et des evenements dans `donnees/visibilite.db`, clefs etrangeres activees, index sur `id_contenu` et `id_session` |

### Tests

| Technologie | Utilisation |
|-------------|-------------|
| **pytest** | Tests unitaires et d'integration couvrant la base de donnees, les routes de collecte, les routes de statistiques et le module d'analyse |

---

## 5. Structure des dossiers

```
Projet_N4_CCC_Anthony_Kamoto/
|
|-- serveur/                        # Code back-end Python/Flask
|   |-- __init__.py
|   |-- appli.py                    # Point d'entree de l'application Flask
|   |-- config.py                   # Configuration (hote, port, chemin BDD)
|   |-- base_de_donnees.py          # Connexion SQLite et creation des tables
|   |
|   |-- modeles/                    # Couche d'acces aux donnees
|   |   |-- __init__.py
|   |   |-- session.py              # CRUD sessions
|   |   |-- evenement.py            # CRUD evenements de visibilite
|   |
|   |-- routes/                     # Blueprints Flask (API + pages)
|   |   |-- __init__.py
|   |   |-- pages.py                # Routes HTML : /, /demo, /tableau-de-bord
|   |   |-- collecte.py             # API collecte : /api/sessions, /api/evenements
|   |   |-- statistiques.py         # API stats : /api/statistiques/*
|   |
|   |-- utilitaires/                # Fonctions transversales
|       |-- __init__.py
|       |-- analyseur.py            # Calculs statistiques (agregations SQL)
|
|-- gabarits/                       # Templates HTML Jinja2
|   |-- page_demo.html              # Page de demonstration avec contenus observes
|   |-- tableau_de_bord.html        # Tableau de bord des statistiques
|
|-- statique/                       # Fichiers statiques (CSS, JS)
|   |-- css/
|   |   |-- style_demo.css          # Styles de la page de demo
|   |   |-- style_tableau_de_bord.css  # Styles du tableau de bord
|   |
|   |-- js/
|       |-- informations_contexte.js   # Detection appareil/navigateur/ecran
|       |-- observateur_visibilite.js  # Observation via IntersectionObserver
|       |-- collecteur_donnees.js      # Tampon, envoi par lots, sendBeacon
|       |-- tableau_de_bord.js         # Graphiques Chart.js et affichage stats
|
|-- donnees/                        # Base de donnees SQLite (generee au lancement)
|   |-- visibilite.db
|
|-- tests/                          # Tests automatises (pytest)
|   |-- test_base_de_donnees.py     # Tests de la couche base de donnees
|   |-- test_routes_collecte.py     # Tests des routes de collecte
|   |-- test_routes_statistiques.py # Tests des routes de statistiques
|   |-- test_analyseur.py           # Tests du module d'analyse
|
|-- docs/                           # Documentation du projet
|   |-- architecture.md             # Ce fichier
|
|-- requirements.txt                # Dependances Python (flask)
|-- Explication_projet.md           # Presentation generale du projet
```
