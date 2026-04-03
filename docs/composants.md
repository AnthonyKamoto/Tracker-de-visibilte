# Description des composants logiciels

Ce document decrit chaque composant du projet de collecte et d'analyse comportementale, ses dependances et ses fonctions ou routes principales.

---

## Serveur (Python / Flask)

### `serveur/appli.py` — Point d'entree de l'application

**Role :** Cree l'instance Flask, initialise la base de donnees et enregistre les trois blueprints (collecte, statistiques, pages). C'est le fichier lance au demarrage du serveur.

**Dependances :** Flask, `config.py`, `base_de_donnees.py`, blueprints definis dans `serveur/routes/`.

**Fonctions principales :**

- `creer_application()` — Fabrique l'application Flask, applique la configuration et enregistre les blueprints.

---

### `serveur/config.py` — Configuration

**Role :** Centralise les parametres de configuration du serveur : chemin vers le fichier de base de donnees SQLite, adresse hote, port d'ecoute et mode debug.

**Dependances :** Aucune dependance externe.

**Parametres exposes :**

- Chemin de la base de donnees SQLite
- Hote et port du serveur
- Activation ou desactivation du mode debug

---

### `serveur/base_de_donnees.py` — Initialisation de la base de donnees

**Role :** Gere la connexion a la base SQLite. Cree les tables necessaires (sessions, evenements) si elles n'existent pas encore, et fournit une fonction utilitaire pour obtenir une connexion.

**Dependances :** `sqlite3` (bibliotheque standard Python), `config.py`.

**Fonctions principales :**

- `initialiser_bdd()` — Cree les tables si elles sont absentes.
- `obtenir_connexion()` — Retourne un objet connexion SQLite pret a l'emploi.

---

### `serveur/modeles/session.py` — Modele Session

**Role :** Fournit les operations CRUD liees aux sessions utilisateur (creation, lecture).

**Dependances :** `base_de_donnees.py` (via `obtenir_connexion()`).

**Fonctions principales :**

- `creer_session(donnees)` — Insere une nouvelle session en base et retourne son identifiant.
- `obtenir_session(id_session)` — Recupere les informations d'une session a partir de son identifiant.

---

### `serveur/modeles/evenement.py` — Modele Evenement

**Role :** Fournit les operations CRUD liees aux evenements de visibilite collectes depuis le navigateur.

**Dependances :** `base_de_donnees.py` (via `obtenir_connexion()`).

**Fonctions principales :**

- `enregistrer_evenement(donnees)` — Insere un evenement unique en base.
- `enregistrer_lot_evenements(liste_evenements)` — Insere plusieurs evenements en une seule transaction (insertion par lots).

---

### `serveur/routes/collecte.py` — Blueprint Collecte

**Role :** Expose les routes d'API qui recoivent les donnees envoyees par le front-end (sessions et evenements).

**Dependances :** Flask (Blueprint), `modeles/session.py`, `modeles/evenement.py`.

**Routes principales :**

- `POST /api/sessions` — Cree une nouvelle session et retourne son identifiant.
- `POST /api/evenements` — Recoit un lot d'evenements de visibilite et les enregistre en base.

---

### `serveur/routes/statistiques.py` — Blueprint Statistiques

**Role :** Expose les routes d'API qui fournissent les donnees statistiques calculees, consommees par le tableau de bord.

**Dependances :** Flask (Blueprint), `modeles/session.py`, `modeles/evenement.py`, `utilitaires/analyseur.py`.

**Routes principales :**

- `GET /api/statistiques/*` — Ensemble de points de terminaison retournant les indicateurs agreges (moyennes, repartitions, classements).

---

### `serveur/routes/pages.py` — Blueprint Pages

**Role :** Sert les pages HTML du projet via le moteur de gabarits Jinja2 integre a Flask.

**Dependances :** Flask (Blueprint, `render_template`), gabarits HTML dans `gabarits/`.

**Routes principales :**

- `GET /` — Page d'accueil.
- `GET /demo` — Page de demonstration avec les contenus surveilles.
- `GET /tableau-de-bord` — Tableau de bord affichant les statistiques.

---

### `serveur/utilitaires/analyseur.py` — Analyseur statistique

**Role :** Contient les fonctions de calcul et d'agregation statistique appelees par le blueprint statistiques.

**Dependances :** `base_de_donnees.py` (via `obtenir_connexion()`).

**Fonctions principales :**

- Calcul des moyennes (temps d'exposition, taux de visibilite).
- Calcul des repartitions (par type d'appareil, par navigateur, par contenu).

---

## Front-end (JavaScript)

### `statique/js/informations_contexte.js` — Detection du contexte utilisateur

**Role :** Module IIFE (Immediately Invoked Function Expression) qui detecte automatiquement les informations contextuelles du visiteur : type d'appareil (mobile, tablette, ordinateur), navigateur utilise et dimensions de l'ecran.

**Dependances :** Aucune (utilise uniquement les API natives du navigateur : `navigator.userAgent`, `window.screen`).

**Donnees exposees :**

- Type d'appareil
- Nom et version du navigateur
- Largeur et hauteur de l'ecran

---

### `statique/js/observateur_visibilite.js` — Observation de la visibilite des elements

**Role :** Module IIFE qui utilise l'API `IntersectionObserver` pour surveiller la visibilite des elements de contenu dans la fenetre du navigateur. Il mesure le temps d'exposition de chaque element et emet des battements de coeur (heartbeat) reguliers.

**Dependances :** API `IntersectionObserver` du navigateur, `collecteur_donnees.js` (pour transmettre les evenements collectes).

**Parametres cles :**

- Seuils d'observation : `[0, 0.25, 0.5, 0.75, 1.0]`
- Chronometre d'exposition par element
- Heartbeat emis toutes les 5 secondes pour chaque element visible

---

### `statique/js/collecteur_donnees.js` — Collecte et envoi des donnees

**Role :** Module IIFE qui gere un tampon (buffer) d'evenements en memoire, les envoie par lots au serveur via des requetes HTTP, et utilise `navigator.sendBeacon` lors de l'evenement `beforeunload` pour garantir l'envoi des derniers evenements avant la fermeture de la page.

**Dependances :** API `fetch` et `navigator.sendBeacon` du navigateur, point de terminaison `POST /api/evenements` du serveur.

**Mecanismes principaux :**

- Mise en tampon des evenements
- Envoi par lots periodique
- Envoi garanti via `sendBeacon` sur `beforeunload`

---

### `statique/js/tableau_de_bord.js` — Script du tableau de bord

**Role :** Script dedie a la page du tableau de bord. Il appelle les quatre points de terminaison statistiques en parallele, puis instancie cinq graphiques Chart.js pour visualiser les resultats.

**Dependances :** Bibliotheque Chart.js, points de terminaison `GET /api/statistiques/*` du serveur.

**Fonctions principales :**

- Appel parallele des 4 API statistiques
- Instanciation et configuration de 5 graphiques Chart.js (barres, camemberts, courbes)
- Mise a jour des cartes de resume et du tableau recapitulatif

---

## Pages HTML (Gabarits Jinja2)

### `gabarits/page_demo.html` — Page de demonstration

**Role :** Page HTML scrollable contenant sept elements de contenu surveilles par l'observateur de visibilite. Elle sert a generer des donnees de visibilite pour tester et alimenter le systeme.

**Dependances :** `statique/css/style_demo.css`, `statique/js/informations_contexte.js`, `statique/js/observateur_visibilite.js`, `statique/js/collecteur_donnees.js`.

**Contenus surveilles (7 elements) :**

- 3 bannieres publicitaires
- 2 blocs de texte
- 2 images

---

### `gabarits/tableau_de_bord.html` — Tableau de bord

**Role :** Page HTML du tableau de bord affichant les statistiques collectees sous forme de cartes de resume, de graphiques interactifs, d'un tableau recapitulatif et d'un filtre par dates.

**Dependances :** `statique/css/style_tableau_de_bord.css`, `statique/js/tableau_de_bord.js`, bibliotheque Chart.js (chargee via CDN).

**Elements de l'interface :**

- 4 cartes de resume (indicateurs cles)
- 5 graphiques Chart.js
- Tableau recapitulatif des donnees
- Filtre par plage de dates

---

## Feuilles de style (CSS)

### `statique/css/style_demo.css` — Style de la page de demonstration

**Role :** Feuille de style dediee a la page de demonstration. Definit la mise en forme de l'en-tete fixe, des sections de contenu en cartes et de l'adaptation responsive aux differentes tailles d'ecran.

**Dependances :** Aucune.

**Caracteristiques :**

- En-tete fixe en haut de page
- Sections en cartes (cards) pour chaque contenu surveille
- Media queries pour l'adaptation responsive

---

### `statique/css/style_tableau_de_bord.css` — Style du tableau de bord

**Role :** Feuille de style dediee au tableau de bord. Definit la grille de mise en page, l'apparence des cartes de resume, des conteneurs de graphiques et du tableau de donnees.

**Dependances :** Aucune.

**Caracteristiques :**

- Grille CSS pour la disposition des elements
- Style des cartes de resume
- Conteneurs dimensionnes pour les graphiques Chart.js
- Mise en forme du tableau recapitulatif
