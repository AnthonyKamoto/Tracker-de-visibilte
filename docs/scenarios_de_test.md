# Scenarios de test

Ce document recense les tests automatises et les scenarios de test manuels du systeme de mesure de visibilite de contenus Web.

---

## Tests unitaires automatises

Le projet comporte **27 tests unitaires** executes avec pytest. Ils couvrent quatre modules.

### Base de donnees (7 tests) - `tests/test_base_de_donnees.py`

| # | Nom du test                      | Description                                                    |
|---|----------------------------------|----------------------------------------------------------------|
| 1 | test_creation_fichier_bdd        | Verifie que le fichier SQLite est cree apres initialisation    |
| 2 | test_table_sessions_existe       | Verifie l'existence de la table `sessions`                     |
| 3 | test_table_evenements_existe     | Verifie l'existence de la table `evenements_visibilite`        |
| 4 | test_colonnes_sessions           | Verifie que la table `sessions` contient les 7 colonnes attendues |
| 5 | test_colonnes_evenements         | Verifie que la table `evenements_visibilite` contient les 9 colonnes attendues |
| 6 | test_insertion_session           | Insere une session et verifie sa presence en BDD               |
| 7 | test_insertion_evenement         | Insere un evenement lie a une session et verifie les donnees   |

### Routes de collecte (7 tests) - `tests/test_routes_collecte.py`

| # | Nom du test                          | Description                                                     |
|---|--------------------------------------|-----------------------------------------------------------------|
| 1 | test_creer_session                   | POST `/api/sessions` cree une session (code 201)                |
| 2 | test_creer_session_sans_donnees      | POST `/api/sessions` sans JSON retourne erreur 400              |
| 3 | test_creer_session_champ_manquant    | POST `/api/sessions` sans `type_appareil` retourne erreur 400   |
| 4 | test_session_dupliquee               | Creer deux fois la meme session retourne 200 (idempotent)       |
| 5 | test_enregistrer_evenements          | POST `/api/evenements` enregistre 2 evenements (code 201)       |
| 6 | test_enregistrer_evenements_sans_session | POST `/api/evenements` sans `id_session` retourne erreur 400 |
| 7 | test_enregistrer_evenements_vides    | POST `/api/evenements` avec liste vide retourne erreur 400      |

### Routes de statistiques (7 tests) - `tests/test_routes_statistiques.py`

| # | Nom du test                     | Description                                                      |
|---|---------------------------------|------------------------------------------------------------------|
| 1 | test_stats_contenus             | GET `/api/statistiques/contenus` retourne les stats par contenu  |
| 2 | test_stats_contenu_detail       | GET `/api/statistiques/contenus/banniere-1` retourne le detail   |
| 3 | test_stats_contenu_inexistant   | GET contenu inexistant retourne 404                              |
| 4 | test_stats_sessions             | GET `/api/statistiques/sessions` retourne le resume correct      |
| 5 | test_stats_appareils            | GET `/api/statistiques/appareils` retourne la repartition        |
| 6 | test_stats_navigateurs          | GET `/api/statistiques/navigateurs` retourne la repartition      |
| 7 | test_stats_bdd_vide             | Les stats avec une BDD vide retournent des listes vides          |

### Analyseur (6 tests) - `tests/test_analyseur.py`

| # | Nom du test                          | Description                                                  |
|---|--------------------------------------|--------------------------------------------------------------|
| 1 | test_statistiques_tous_contenus      | Calcule les stats pour tous les contenus (2 contenus)        |
| 2 | test_statistiques_contenu_specifique | Calcule les stats pour un contenu precis (visibilite = 0.9)  |
| 3 | test_statistiques_contenu_inexistant | Retourne None pour un contenu inexistant                     |
| 4 | test_resume_sessions                 | Resume correct : 2 sessions, 3 evenements                    |
| 5 | test_repartition_appareils           | Repartition correcte : ordinateur et mobile                  |
| 6 | test_repartition_navigateurs         | Repartition correcte : Chrome 120 et Safari 17               |

### Executer les tests

```bash
python -m pytest tests/ -v
```

---

## Scenarios de test manuels

Ces scenarios permettent de verifier le bon fonctionnement de bout en bout dans un navigateur.

### Scenario 1 : Collecte de donnees de visibilite

**Objectif** : verifier que les evenements de visibilite sont correctement collectes et stockes.

1. Lancer le serveur : `python serveur/appli.py`
2. Ouvrir http://localhost:5000/demo dans un navigateur
3. Observer la console du navigateur (F12) : un message confirme la creation de la session
4. Scroller lentement vers le bas pour exposer chaque contenu surveille
5. Attendre quelques secondes sur chaque contenu pour generer des durees d'exposition
6. Verifier dans la console du navigateur que les evenements sont envoyes au serveur (requetes POST visibles dans l'onglet Reseau)

**Resultat attendu** : les evenements de visibilite sont envoyes au serveur avec les pourcentages et durees corrects.

### Scenario 2 : Consultation du tableau de bord

**Objectif** : verifier que le tableau de bord affiche les donnees collectees.

1. Apres avoir effectue le scenario 1, ouvrir http://localhost:5000/tableau-de-bord
2. Verifier la presence des 5 graphiques : visibilite moyenne par contenu, duree d'exposition moyenne, repartition par type d'appareil, repartition par navigateur, evolution temporelle
3. Verifier que les valeurs affichees correspondent aux donnees collectees
4. Tester le filtre de dates : selectionner une plage et verifier que les graphiques se mettent a jour

**Resultat attendu** : les graphiques affichent correctement les donnees collectees, le filtre de dates fonctionne.

### Scenario 3 : Verification en base de donnees

**Objectif** : verifier que les donnees sont correctement stockees en BDD.

1. Apres avoir effectue le scenario 1, ouvrir le fichier `donnees/visibilite.db` avec un outil SQLite (DB Browser for SQLite, ou la commande `sqlite3`)
2. Verifier la table `sessions` : une ligne doit correspondre a la session de test
3. Verifier la table `evenements_visibilite` : plusieurs lignes doivent etre presentes avec des valeurs coherentes de `pourcentage_visibilite` et `duree_exposition_ms`

**Resultat attendu** : les tables contiennent les donnees attendues avec les bons types et valeurs.

---

## Limites techniques connues

| Limite                                  | Impact                                                          | Contournement eventuel                          |
|-----------------------------------------|-----------------------------------------------------------------|-------------------------------------------------|
| SQLite mono-ecriture                    | En cas d'acces concurrents eleves, des erreurs de verrouillage peuvent survenir | Migrer vers PostgreSQL pour la production       |
| IntersectionObserver non supporte       | Les tres vieux navigateurs (IE, anciens mobiles) ne detectent pas la visibilite | Utiliser un polyfill ou exiger un navigateur moderne |
| Pas d'authentification                  | Le tableau de bord et l'API sont accessibles sans restriction   | Ajouter un systeme d'authentification           |
| Pas de pagination sur les statistiques  | Les performances peuvent se degrader avec un tres grand volume de donnees | Implementer la pagination cote API              |
