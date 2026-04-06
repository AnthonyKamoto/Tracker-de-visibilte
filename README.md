# Tracker de visibilite

Projet pedagogique realise pour la Fondation CCC (2026).

Ce systeme mesure la visibilite reelle des contenus affiches sur une page web : pourcentage de surface visible, duree d'exposition et informations contextuelles (appareil, navigateur, resolution). Les donnees collectees sont restituees sur un tableau de bord interactif independant.

---

## Fonctionnalites cles

- **Detection de la visibilite** : utilisation de l'API IntersectionObserver pour detecter en temps reel si un contenu est visible dans le viewport du navigateur
- **Duree d'exposition** : mesure du temps pendant lequel chaque contenu reste visible
- **Informations contextuelles** : collecte automatique du type d'appareil, du navigateur et de la resolution d'ecran
- **Tableau de bord** : 5 graphiques interactifs (Chart.js) avec filtre par plage de dates, rafraichissement automatique et indicateur de connexion
- **Architecture separee** : le site d'actualites (port 5000) et le dashboard (port 5001) fonctionnent comme deux applications independantes communiquant via API REST et CORS

---

## Stack technique

| Composant       | Technologie                |
|-----------------|----------------------------|
| Back-end        | Python 3.10+ / Flask       |
| Base de donnees | SQLite                     |
| Front-end       | JavaScript / IntersectionObserver |
| Graphiques      | Chart.js                   |
| Templates       | Jinja2                     |
| CORS            | Flask-CORS                 |
| Tests           | pytest (30 tests)          |

---

## Compatibilite

Le projet fonctionne sur **Windows**, **macOS** et **Linux**. Aucune dependance specifique a un systeme d'exploitation n'est requise. Python, SQLite et les navigateurs modernes sont disponibles sur les trois plateformes.

---

## Installation rapide

### 1. Cloner et preparer

```bash
git clone <url-du-depot>
cd Projet_N4_CCC_Anthony_Kamoto
python -m venv venv
```

### 2. Activer l'environnement virtuel

| Systeme       | Commande                        |
|---------------|----------------------------------|
| Windows (PS)  | `venv\Scripts\Activate.ps1`      |
| macOS / Linux | `source venv/bin/activate`       |

### 3. Installer les dependances

```bash
pip install -r requirements.txt
```

### 4. Lancer les serveurs

**Option A — Scripts automatiques (recommande) :**

```powershell
# Windows
.\lancer.ps1
```

```bash
# macOS / Linux
./lancer.sh
```

**Option B — Lancement manuel (deux terminaux) :**

```bash
# Terminal 1 — Serveur d'actualites + API
python serveur/appli.py

# Terminal 2 — Dashboard
python dashboard/appli.py
```

---

## Pages de l'application

| Page                  | URL                           | Description                              |
|-----------------------|-------------------------------|------------------------------------------|
| Site d'actualites     | http://localhost:5000          | Site avec 21 contenus surveilles         |
| Tableau de bord       | http://localhost:5001          | Dashboard avec graphiques et statistiques|

---

## Structure du projet

```
📁 Projet_N4_CCC_Anthony_Kamoto/
    📁 serveur/                               # Serveur principal (port 5000)
        🐍 appli.py                           # Point d'entree Flask + CORS
        🐍 config.py                          # Configuration (port, chemin BDD)
        🐍 base_de_donnees.py                 # Initialisation SQLite
        📁 modeles/
            🐍 session.py                     # Modele de session
            🐍 evenement.py                   # Modele d'evenement
        📁 routes/
            🐍 collecte.py                    # API de collecte (POST)
            🐍 statistiques.py                # API de statistiques (GET)
            🐍 pages.py                       # Route du site d'actualites
        📁 utilitaires/
            🐍 analyseur.py                   # Calcul des statistiques
    📁 dashboard/                             # Dashboard independant (port 5001)
        🐍 appli.py                           # Point d'entree Flask du dashboard
        🐍 config.py                          # Configuration (port, URL serveur)
        📁 templates/
            🌐 tableau_de_bord.html           # Page du tableau de bord
        📁 static/
            📁 css/
                🎨 style_tableau_de_bord.css  # Styles du dashboard
            📁 js/
                ⚡ tableau_de_bord.js          # Graphiques Chart.js
    📁 templates/
        🌐 page_demo.html                     # Site d'actualites (21 elements surveilles)
    📁 static/
        📁 css/
            🎨 style_demo.css                 # Styles du site d'actualites
        📁 js/
            ⚡ observateur_visibilite.js      # Detection de visibilite (IntersectionObserver)
            ⚡ collecteur_donnees.js          # Envoi des donnees au serveur
            ⚡ informations_contexte.js       # Detection appareil/navigateur
    📁 donnees/                               # Base de donnees SQLite (cree automatiquement)
        🗄️ visibilite.db
    📁 tests/                                 # 30 tests unitaires (pytest)
        🐍 test_base_de_donnees.py            # Tests du module BDD (7 tests)
        🐍 test_routes_collecte.py            # Tests des routes de collecte (7 tests)
        🐍 test_routes_statistiques.py        # Tests des routes de statistiques (7 tests)
        🐍 test_analyseur.py                  # Tests de l'analyseur (6 tests)
        🐍 test_dashboard.py                  # Tests du dashboard (3 tests)
    📁 docs/
        📝 architecture.md                    # Architecture du systeme
        📝 base_de_donnees.md                 # Schema de la BDD
        📝 guide_installation.md              # Guide d'installation
        📝 rapport_synthese.md                # Rapport de synthese
    🪟 lancer.ps1                             # Script de lancement (Windows)
    🐧 lancer.sh                              # Script de lancement (macOS/Linux)
    📋 requirements.txt                       # Dependances Python
```

---

## Lancer les tests

```bash
python -m pytest tests/ -v
```

30 tests couvrant : base de donnees (7), routes de collecte (7), routes de statistiques (7), analyseur (6), dashboard (3).

---

## Licence

Projet pedagogique realise dans le cadre de la Fondation CCC - 2026.
Usage educatif uniquement.
