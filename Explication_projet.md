# Projet de formation des formateurs

# Projet N° 4

## Développement d’un système de mesure de visibilité de contenus Web

## 2026 Version PI. 03 .2 6 FCCC-V003 1 6 Mars 2026


**Développement d’un système de mesure de
visibilité de contenus Web**

**1. Contexte du projet**

La transformation numérique des médias et des plateformes éducatives repose largement
sur la capacité à **mesurer l’engagement réel des utilisateurs** face aux contenus diffusés en
ligne. Dans l’écosystème web actuel, un contenu (image, bannière, vidéo, bloc d’information)
peut être techniquement chargé dans une page sans être réellement visible par l’utilisateur.

Cette situation concerne notamment :

- les publicités numériques,
- les contenus pédagogiques,
- les supports de sensibilisation en ligne,
- les contenus informatifs diffusés sur des plateformes web.

Dans ce contexte, la **Fondation Children Coding Club (CCC)** souhaite développer, dans le cadre
de la montée en compétence de ses formateurs, un **prototype technologique permettant de
mesurer la visibilité réelle d’un contenu web** et d’en analyser les données.

Ce projet s’inscrit dans la stratégie globale de la fondation visant à :

- renforcer les compétences techniques de ses formateurs,
- développer des capacités de conception de solutions numériques,
- préparer la réalisation de futurs projets technologiques pour des partenaires
    institutionnels, éducatifs ou privés,
- structurer une culture d’ingénierie logicielle au sein de la fondation.

Le projet constitue donc **un exercice pédagogique avancé** , mais également **un prototype
potentiellement valorisable** dans les activités futures de CCC.

**2. Objectifs du projet**

→ **Objectif général**

Concevoir et développer une solution web capable de :

- détecter la visibilité réelle d’un contenu dans une page web,
- mesurer le **taux de visibilité et la durée d’exposition** ,
- transmettre ces informations à un serveur,
- enregistrer les données dans une base de données,
- produire des indicateurs exploitables sur la consultation des contenus.

→ **Objectifs pédagogiques**

À travers ce projet, les formateurs devront démontrer leur capacité à :

- analyser un besoin technique réel,
- concevoir une architecture logicielle cohérente,
- développer une solution web complète (front-end / back-end),
- exploiter Python dans un environnement serveur et analytique,
- structurer et exploiter des données,
- documenter un projet technique,
- travailler en équipe sur un projet numérique.
**3. Architecture technique de référence**

Le projet devra reposer sur une architecture simple et cohérente intégrant :

**Front-end**

- page web de test contenant les contenus à surveiller
- script de détection de visibilité dans le navigateur

**Back-end**

- serveur Python recevant les données collectées
- API permettant la transmission des mesures

**Base de données**

- stockage des événements de visibilité
- structuration des données collectées

**Exploitation des données**

- analyse des résultats
- production d’indicateurs statistiques
- visualisation simple ou tableau de bord

**4. Organisation pédagogique du projet**

Afin de tenir compte des différences de niveau technique au sein de l’équipe de formateurs,
le projet est structuré en **deux niveaux de réalisation** :

- **Niveau 1 : Prototype fonctionnel**
- **Niveau 2 : Prototype avancé**

Les participants pourront être répartis entre les deux niveaux selon leurs compétences et leur
rôle dans le projet.

**5. Niveau 1 – Prototype fonctionnel**

→ **Objectif**

Développer une solution simple permettant de démontrer le fonctionnement complet du
système de mesure de visibilité.

→ **Travaux attendus**

Le groupe devra :

1. Concevoir une page web contenant plusieurs contenus visuels à surveiller.
2. Identifier les contenus à mesurer à l’aide d’un attribut ou d’une classe spécifique.
3. Développer un mécanisme de détection de visibilité dans le navigateur.
4. Mesurer le pourcentage de visibilité d’un contenu à l’écran.
5. Transmettre les données de visibilité vers un serveur Python.
6. Enregistrer les mesures dans une base de données.
7. Afficher ou exporter les résultats collectés.

→ **Résultat attendu**

Un prototype fonctionnel capable de :

- détecter la visibilité d’un contenu,
- transmettre les données au serveur,
- enregistrer les mesures dans une base de données,
- permettre la consultation simple des résultats.

**6. Niveau 2 – Prototype avancé**

→ **Objectif**

Concevoir une version plus robuste et structurée du système, permettant une analyse plus
complète des données collectées.

→ **Travaux attendus**

Le groupe devra :

1. Améliorer la précision de la mesure de visibilité.
2. Calculer le **temps réel d’exposition d’un contenu**.
3. Gérer plusieurs contenus surveillés simultanément.
4. Structurer l’API de collecte des données.
5. Mettre en place une base de données organisée.
6. Ajouter des informations contextuelles aux mesures :
    - type d’appareil
    - taille d’écran
    - navigateur
    - page consultée
7. Produire des statistiques exploitables.
8. Mettre en place un tableau de bord simple pour visualiser les données.

→ **Résultat attendu**

Une solution avancée capable de :

- mesurer précisément la visibilité des contenus,
- analyser les comportements de consultation,
- produire des indicateurs exploitables.

**7. Livrables attendus**

Chaque groupe devra produire les éléments suivants.

→ **Solution technique**

- code source complet du projet
- serveur Python fonctionnel
- base de données structurée
- page web de démonstration

→ **Documentation technique**

- description de l’architecture du système
- description des composants logiciels
- description de la structure de la base de données
- guide d’installation et d’exécution

→ **Tests**

- description des scénarios de test réalisés
- résultats des tests
- identification des limites techniques

→ **Rapport de synthèse**

Le rapport devra présenter :

- le problème traité
- l’architecture choisie
- les technologies utilisées
- les résultats obtenus
- les pistes d’amélioration

→ **Démonstration finale**

Chaque groupe devra présenter :

- le fonctionnement de la solution
- les choix techniques réalisés
- les résultats obtenus
- les perspectives d’évolution.

**8. Planning recommandé**

**Phase 1 – Cadrage du projet**

- compréhension du problème
- définition des indicateurs
- conception de l’architecture

**Phase 2 – Développement initial**

- création de la page web de test
- mise en place du mécanisme de détection
- premiers tests de visibilité

**Phase 3 – Mise en place du serveur**

- développement de l’API Python
- réception des données
- stockage en base

**Phase 4 – Stabilisation du prototype**

- tests multi-navigateurs
- tests multi-écrans
- validation du flux complet

**Phase 5 – Exploitation des données**

- analyse des mesures collectées
- génération de statistiques
- création d’un tableau de bord simple

**Phase 6 – Finalisation**

- documentation
- préparation de la démonstration
- présentation finale du projet


**Développement d’un système de mesure de
visibilité de contenus Web**

**9. Critères d’évaluation**

Les projets seront évalués selon les critères suivants.

→ **Compréhension du problème**

Capacité à analyser et formaliser le besoin technique.

→ **Qualité de l’architecture**

Cohérence et lisibilité de la structure du projet.

→ **Fonctionnement de la solution**

Capacité du système à mesurer et enregistrer correctement les données.

→ **Qualité du code**

Clarté, organisation et maintenabilité du code.

→ **Exploitation des données**

Capacité à produire des indicateurs utiles.

→ **Documentation**

Qualité de la documentation technique et du rapport final.

→ **Présentation**

Clarté et qualité de la démonstration du projet.

**10. Guide global de réalisation**

Les équipes devront structurer leur travail selon les principes suivants :

1. **Comprendre le besoin avant de coder** : définir clairement ce qui constitue une visibilité
    réelle d’un contenu.
2. **Concevoir l’architecture globale** du système avant d’entamer le développement.
3. **Développer progressivement** les différents composants.
4. **Tester régulièrement** le fonctionnement du système.
5. **Documenter chaque étape importante** du projet.
6. **Valider collectivement les choix techniques** au sein de l’équipe.
7. **Produire un projet démontrable et reproductible**.

Le projet devra refléter une démarche d’ingénierie logicielle structurée, conforme aux
standards de développement attendus dans les projets numériques professionnels.

