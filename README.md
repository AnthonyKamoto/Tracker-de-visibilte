# Tracker de visibilite

Projet pedagogique realise pour la Fondation CCC (2026).

Ce systeme mesure la visibilite reelle des contenus affiches sur une page web : pourcentage de surface visible, duree d'exposition et informations contextuelles (appareil, navigateur, resolution). Les donnees collectees sont restituees sur un tableau de bord interactif.

---

## Fonctionnalites cles

- **Detection de la visibilite** : utilisation de l'API IntersectionObserver pour detecter en temps reel si un contenu est visible dans le viewport du navigateur
- **Duree d'exposition** : mesure du temps pendant lequel chaque contenu reste visible
- **Informations contextuelles** : collecte automatique du type d'appareil, du navigateur et de la resolution d'ecran
- **Tableau de bord** : 5 graphiques interactifs (Chart.js) avec filtre par plage de dates

---

## Stack technique

| Composant       | Technologie                |
|-----------------|----------------------------|
| Back-end        | Python 3.10+ / Flask       |
| Base de donnees | SQLite                     |
| Front-end       | JavaScript / IntersectionObserver |
| Graphiques      | Chart.js                   |
| Templates       | Jinja2                     |
| Tests           | pytest (27 tests)          |

---

## Compatibilite

Le projet fonctionne sur **Windows**, **macOS** et **Linux**. Aucune dependance specifique a un systeme d'exploitation n'est requise. Python, SQLite et les navigateurs modernes sont disponibles sur les trois plateformes.

---

## Installation rapide

### Windows (PowerShell)

```powershell
git clone <url-du-depot>
cd Projet_N4_CCC_Anthony_Kamoto
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python serveur/appli.py
```

### macOS / Linux (Bash)

```bash
git clone <url-du-depot>
cd Projet_N4_CCC_Anthony_Kamoto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python serveur/appli.py
```

Le serveur demarre sur http://localhost:5000.

---

## Pages de l'application

| Page                  | URL                                   |
|-----------------------|---------------------------------------|
| Page de demonstration | http://localhost:5000/demo            |
| Tableau de bord       | http://localhost:5000/tableau-de-bord |

---

## Structure du projet

```
Projet_N4_CCC_Anthony_Kamoto/
    venv/                              # Environnement virtuel Python
    serveur/
        appli.py                       # Point d'entree Flask
        config.py                      # Configuration (port, chemin BDD)
        base_de_donnees.py             # Initialisation SQLite
        modeles/
            session.py                 # Modele de session
            evenement.py               # Modele d'evenement
        routes/
            collecte.py                # API de collecte (POST sessions, evenements)
            statistiques.py            # API de statistiques (GET stats)
            pages.py                   # Routes des pages HTML
        utilitaires/
            analyseur.py               # Calcul des statistiques
    templates/
        page_demo.html                 # Page de demonstration
        tableau_de_bord.html           # Tableau de bord
    static/
        css/
            style_demo.css             # Style de la page demo
            style_tableau_de_bord.css  # Style du tableau de bord
        js/
            observateur_visibilite.js  # Detection de visibilite (IntersectionObserver)
            collecteur_donnees.js      # Envoi des donnees au serveur
            informations_contexte.js   # Detection appareil/navigateur
            tableau_de_bord.js         # Graphiques Chart.js
    donnees/                           # Base de donnees SQLite (cree automatiquement)
    tests/
        test_base_de_donnees.py        # Tests du module BDD (7 tests)
        test_routes_collecte.py        # Tests des routes de collecte (7 tests)
        test_routes_statistiques.py    # Tests des routes de statistiques (7 tests)
        test_analyseur.py              # Tests de l'analyseur (6 tests)
    docs/
        base_de_donnees.md             # Schema de la BDD
        architecture.md                # Architecture du systeme
        guide_installation.md          # Guide d'installation
        rapport_synthese.md            # Rapport de synthese
    requirements.txt                   # Dependances Python
```

---

## Lancer les tests

```bash
python -m pytest tests/ -v
```

27 tests couvrant : base de donnees (7), routes de collecte (7), routes de statistiques (7), analyseur (6).

---

## Licence

Projet pedagogique realise dans le cadre de la Fondation CCC - 2026.
Usage educatif uniquement.
