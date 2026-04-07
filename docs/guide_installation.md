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
- **flask-cors** : gestion des requetes cross-origin entre le site et le dashboard
- **pytest** : framework de tests unitaires

### 4. Lancer les serveurs

**Option A — Scripts automatiques (recommande) :**

Les scripts lancent les deux serveurs simultanement et gerent l'arret propre avec Ctrl+C.

```powershell
# Windows (PowerShell)
.\lancer.ps1
```

```bash
# macOS / Linux
chmod +x lancer.sh
./lancer.sh
```

**Option B — Lancement manuel (deux terminaux) :**

```bash
# Terminal 1 — Serveur d'actualites + API (port 5000)
python serveur/appli.py

# Terminal 2 — Dashboard (port 5001)
python dashboard/appli.py
```

Le serveur d'actualites demarre sur le port 5000 et le dashboard sur le port 5001. Un message de confirmation s'affiche dans chaque terminal.

---

## Acces a l'application

Une fois les serveurs lances, ouvrir un navigateur et acceder aux pages suivantes :

| Page                  | URL                           | Description                                              |
|-----------------------|-------------------------------|----------------------------------------------------------|
| Site d'actualites     | http://localhost:5000         | Site avec 21 contenus surveilles pour generer des donnees|
| Tableau de bord       | http://localhost:5001         | Dashboard avec graphiques, statistiques et auto-refresh  |

### Site d'actualites

Le site d'actualites est une page complete de type journal en ligne avec 21 elements HTML surveilles (bannieres, articles, images, video, FAQ, newsletter, widgets). Il suffit de scroller pour generer des evenements de visibilite envoyes au serveur.

### Tableau de bord

Le tableau de bord est une application independante qui consomme les API du serveur principal. Il affiche les statistiques collectees sous forme de graphiques interactifs (Chart.js) : visibilite moyenne par contenu, duree d'exposition, repartition par appareil et navigateur. Il dispose d'un indicateur de connexion au serveur et d'un mode de rafraichissement automatique (toutes les 10 secondes).

---

## Lancer les tests

Le projet dispose de 42 tests unitaires repartis en 5 modules. Pour les executer :

```bash
python -m pytest tests/ -v
```

Resultat attendu :

```
tests/test_analyseur.py ............                    [  6 passed]
tests/test_base_de_donnees.py .......                   [  7 passed]
tests/test_dashboard.py ...                             [  3 passed]
tests/test_routes_collecte.py .................          [ 17 passed]
tests/test_routes_statistiques.py .........              [  9 passed]

========================= 42 passed =========================
```

---

## Structure du projet

```
Projet_N4_CCC_Anthony_Kamoto/
    serveur/                          # Serveur principal (port 5000)
        appli.py                      # Point d'entree Flask + CORS
        config.py                     # Configuration (port, chemin BDD)
        base_de_donnees.py            # Initialisation SQLite
        modeles/                      # Modeles de donnees (session, evenement)
        routes/                       # Routes API (collecte, statistiques, pages)
        utilitaires/                  # Analyseur de statistiques
    dashboard/                        # Dashboard independant (port 5001)
        appli.py                      # Point d'entree Flask du dashboard
        config.py                     # Configuration (port, URL serveur)
        templates/                    # Template du tableau de bord
        static/                       # CSS et JS du dashboard
    templates/                         # Template du site d'actualites
    static/
        css/                          # Feuilles de style du site
        js/                           # Scripts front-end (observateur, collecteur)
    donnees/                          # Base de donnees SQLite (cree au lancement)
    tests/                            # 42 tests unitaires pytest
    docs/                             # Documentation du projet
    lancer.ps1                        # Script de lancement (Windows)
    lancer.sh                         # Script de lancement (macOS/Linux)
    requirements.txt                  # Dependances Python
```

