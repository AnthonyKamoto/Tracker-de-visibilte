# Base de donnees - Schema SQLite

Ce document decrit le schema de la base de donnees SQLite utilisee par le systeme de mesure de visibilite de contenus Web.

Le fichier de base de donnees est stocke dans `donnees/visibilite.db`. Il est cree automatiquement au premier lancement de l'application.

---

## Table `sessions`

Enregistre les informations de chaque session de navigation d'un visiteur.

| Colonne          | Type    | Contrainte                                | Description                                    |
|------------------|---------|-------------------------------------------|------------------------------------------------|
| id_session       | TEXT    | PRIMARY KEY                               | Identifiant unique de la session (UUID)        |
| type_appareil    | TEXT    | NOT NULL                                  | Type d'appareil : ordinateur, mobile, tablette |
| largeur_ecran    | INTEGER |                                           | Largeur de l'ecran en pixels                   |
| hauteur_ecran    | INTEGER |                                           | Hauteur de l'ecran en pixels                   |
| navigateur       | TEXT    |                                           | Nom et version du navigateur                   |
| page_consultee   | TEXT    |                                           | URL de la page consultee                       |
| date_debut       | TEXT    | NOT NULL, DEFAULT datetime('now')         | Date et heure de debut de session (ISO 8601)   |

### Commande SQL

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id_session TEXT PRIMARY KEY,
    type_appareil TEXT NOT NULL,
    largeur_ecran INTEGER,
    hauteur_ecran INTEGER,
    navigateur TEXT,
    page_consultee TEXT,
    date_debut TEXT NOT NULL DEFAULT (datetime('now'))
);
```

---

## Table `evenements_visibilite`

Stocke chaque evenement de visibilite detecte par l'IntersectionObserver sur le navigateur du visiteur.

| Colonne                 | Type    | Contrainte                                    | Description                                           |
|-------------------------|---------|-----------------------------------------------|-------------------------------------------------------|
| id_evenement            | INTEGER | PRIMARY KEY AUTOINCREMENT                     | Identifiant auto-incremente de l'evenement            |
| id_session              | TEXT    | NOT NULL, FOREIGN KEY -> sessions(id_session) | Reference vers la session du visiteur                 |
| id_contenu              | TEXT    | NOT NULL                                      | Identifiant du contenu surveille (ex: banniere-1)     |
| type_contenu            | TEXT    |                                               | Type du contenu : banniere, texte, image, video, etc. |
| pourcentage_visibilite  | REAL    | NOT NULL                                      | Ratio de visibilite entre 0.0 et 1.0                  |
| duree_exposition_ms     | INTEGER | DEFAULT 0                                     | Duree d'exposition en millisecondes                   |
| horodatage_debut        | TEXT    |                                               | Horodatage du debut de visibilite (ISO 8601)          |
| horodatage_fin          | TEXT    |                                               | Horodatage de fin de visibilite (ISO 8601)            |
| date_enregistrement     | TEXT    | NOT NULL, DEFAULT datetime('now')             | Date d'enregistrement cote serveur (ISO 8601)         |

### Commande SQL

```sql
CREATE TABLE IF NOT EXISTS evenements_visibilite (
    id_evenement INTEGER PRIMARY KEY AUTOINCREMENT,
    id_session TEXT NOT NULL,
    id_contenu TEXT NOT NULL,
    type_contenu TEXT,
    pourcentage_visibilite REAL NOT NULL,
    duree_exposition_ms INTEGER DEFAULT 0,
    horodatage_debut TEXT,
    horodatage_fin TEXT,
    date_enregistrement TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (id_session) REFERENCES sessions(id_session)
);
```

---

## Index

Deux index sont crees pour accelerer les requetes les plus frequentes (recherche par contenu et par session).

```sql
CREATE INDEX IF NOT EXISTS idx_evenements_contenu
ON evenements_visibilite(id_contenu);

CREATE INDEX IF NOT EXISTS idx_evenements_session
ON evenements_visibilite(id_session);
```

---

## Relations

```
sessions (1) ----< (N) evenements_visibilite
   PK: id_session         FK: id_session -> sessions(id_session)
```

Une session peut avoir zero ou plusieurs evenements de visibilite. Chaque evenement est obligatoirement rattache a une session existante grace a la contrainte de cle etrangere activee par `PRAGMA foreign_keys = ON`.

---

## Remarques techniques

- **Format des dates** : toutes les dates sont stockees au format ISO 8601 (`YYYY-MM-DD HH:MM:SS`) pour garantir un tri chronologique correct.
- **Cles etrangeres** : activees explicitement a chaque connexion via `PRAGMA foreign_keys = ON`.
- **Delai d'attente** : configure a 10 secondes (`timeout=10`) pour gerer les acces concurrents limites de SQLite.
- **Chemin du fichier** : `donnees/visibilite.db` (relatif a la racine du projet). Le repertoire `donnees/` est cree automatiquement s'il n'existe pas.
