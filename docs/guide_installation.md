# Guide d'installation et d'execution

Ce guide explique comment installer, configurer et lancer le Tracker de visibilite.

---

## Prerequis

| Prerequis            | Version minimale | Remarque                                                  |
|----------------------|------------------|-----------------------------------------------------------|
| Python               | 3.10+            | `python --version` (Windows) ou `python3 --version` (macOS/Linux) |
| pip                  | 21+              | Gestionnaire de paquets Python (inclus avec Python)       |
| git                  | 2.x+             | Pour cloner le depot                                      |
| Navigateur moderne   | ---              | Chrome 51+, Firefox 55+, Edge 15+, Safari 12.1+ (support IntersectionObserver) |

> SQLite est inclus dans la bibliotheque standard de Python : aucune installation supplementaire n'est requise pour la base de donnees.

---

## Systemes d'exploitation supportes

Le projet est compatible avec :

| Systeme             | Teste | Remarques                                           |
|---------------------|-------|-----------------------------------------------------|
| **Windows 10/11**   | Oui   | PowerShell ou cmd                                   |
| **macOS 12+**       | Oui   | Terminal (Bash / Zsh)                                |
| **Linux (Ubuntu, Debian, Fedora...)** | Oui | Terminal Bash |

Toutes les dependances sont multiplateformes. Le code Python utilise exclusivement `os.path` pour les chemins de fichiers, ce qui garantit la portabilite.

---

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-depot>
cd Projet_N4_CCC_Anthony_Kamoto
```

### 2. Creer et activer l'environnement virtuel

**Creation (identique sur tous les OS) :**

```bash
python -m venv venv
```

> Sur macOS/Linux, utiliser `python3` si `python` n'est pas reconnu.

**Activation selon le systeme et le terminal :**

| Systeme         | Terminal     | Commande                          |
|-----------------|-------------|-----------------------------------|
| Windows         | PowerShell  | `venv\Scripts\Activate.ps1`       |
| Windows         | cmd         | `venv\Scripts\activate.bat`       |
| Windows         | Git Bash    | `source venv/Scripts/activate`    |
| macOS / Linux   | Bash / Zsh  | `source venv/bin/activate`        |

> Si PowerShell bloque l'activation, executer d'abord :
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

Une fois active, le prefixe `(venv)` apparait dans le terminal.

### 3. Installer les dependances Python

```bash
pip install -r requirements.txt
```

Les dependances du projet sont :

- **flask** : framework web leger pour le serveur HTTP et l'API REST

### 4. Lancer le serveur

```bash
python serveur/appli.py
```

Le serveur demarre sur le port 5000. Un message de confirmation s'affiche dans le terminal :

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## Acces a l'application

Une fois le serveur lance, ouvrir un navigateur et acceder aux pages suivantes :

| Page                  | URL                                      | Description                                       |
|-----------------------|------------------------------------------|---------------------------------------------------|
| Page de demonstration | http://localhost:5000/demo               | Page avec 7 contenus surveilles pour tester la collecte |
| Tableau de bord       | http://localhost:5000/tableau-de-bord    | Dashboard avec graphiques et statistiques          |

### Page de demonstration

La page de demonstration contient plusieurs elements HTML (bannieres, textes, images, videos) dont la visibilite est automatiquement surveillee. Il suffit de scroller pour generer des evenements de visibilite envoyes au serveur.

### Tableau de bord

Le tableau de bord affiche les statistiques collectees sous forme de graphiques interactifs (Chart.js) : visibilite moyenne par contenu, duree d'exposition, repartition par appareil et navigateur, avec un filtre par plage de dates.

---

## Lancer les tests

Le projet dispose de 27 tests unitaires repartis en 4 modules. Pour les executer :

```bash
python -m pytest tests/ -v
```

Resultat attendu :

```
tests/test_analyseur.py ............                    [  6 passed]
tests/test_base_de_donnees.py .......                   [  7 passed]
tests/test_routes_collecte.py .......                   [  7 passed]
tests/test_routes_statistiques.py .......               [  7 passed]

========================= 27 passed =========================
```

---

## Structure du projet

```
Projet_N4_CCC_Anthony_Kamoto/
    venv/                         # Environnement virtuel Python
    serveur/
        appli.py                  # Point d'entree Flask
        config.py                 # Configuration (port, chemin BDD)
        base_de_donnees.py        # Initialisation SQLite
        modeles/                  # Modeles de donnees (session, evenement)
        routes/                   # Routes API (collecte, statistiques, pages)
        utilitaires/              # Analyseur de statistiques
    templates/                     # Templates HTML (Jinja2)
    static/
        css/                      # Feuilles de style
        js/                       # Scripts front-end (observateur, collecteur)
    donnees/                      # Base de donnees SQLite (cree au lancement)
    tests/                        # Tests unitaires pytest
    docs/                         # Documentation du projet
    requirements.txt              # Dependances Python
```

---

## Problemes courants

| Probleme                        | OS       | Solution                                                      |
|---------------------------------|----------|---------------------------------------------------------------|
| `ModuleNotFoundError: flask`    | Tous     | Verifier que le venv est active, puis `pip install -r requirements.txt` |
| `python` non reconnu            | macOS/Linux | Utiliser `python3` au lieu de `python`                     |
| Activation PowerShell bloquee   | Windows  | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Port 5000 deja utilise          | Tous     | Modifier `PORT` dans `serveur/config.py`                      |
| Port 5000 pris par AirPlay      | macOS    | Desactiver AirPlay Receiver dans Preferences systeme, ou changer le port |
| Base de donnees verrouillee     | Tous     | Arreter les autres instances du serveur                       |
| IntersectionObserver non supporte | Tous   | Utiliser un navigateur moderne (Chrome 51+, Firefox 55+)      |
