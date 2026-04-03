/**
 * Module principal d'observation de la visibilité des contenus.
 * Utilise IntersectionObserver pour détecter l'entrée/sortie des éléments
 * et mesure la durée d'exposition de chaque contenu.
 */

const ObservateurVisibilite = (function () {

    // État de chaque contenu surveillé (Map : id_contenu → objet état)
    const etatContenus = new Map();

    // Seuils de visibilité déclenchant le callback
    const SEUILS = [0, 0.25, 0.5, 0.75, 1.0];

    /**
     * Callback appelé par l'IntersectionObserver quand un contenu
     * franchit un seuil de visibilité.
     */
    function gererChangementVisibilite(entrees) {
        const maintenant = Date.now();

        entrees.forEach(function (entree) {
            const element = entree.target;
            const idContenu = element.getAttribute('data-contenu-id');
            const typeContenu = element.getAttribute('data-type-contenu');

            if (!idContenu) return;

            // Créer l'état si première observation
            if (!etatContenus.has(idContenu)) {
                etatContenus.set(idContenu, {
                    idContenu: idContenu,
                    typeContenu: typeContenu,
                    estVisible: false,
                    horodatageDebut: null,
                    derniereVisibilite: 0,
                    dureeAccumulee: 0
                });
            }

            const etat = etatContenus.get(idContenu);

            if (entree.isIntersecting) {
                // Le contenu entre dans le viewport ou change de ratio
                if (!etat.estVisible) {
                    // Début de visibilité
                    etat.estVisible = true;
                    etat.horodatageDebut = maintenant;
                }
                etat.derniereVisibilite = entree.intersectionRatio;

            } else {
                // Le contenu sort du viewport
                if (etat.estVisible) {
                    const dureeExposition = maintenant - etat.horodatageDebut;
                    etat.dureeAccumulee += dureeExposition;

                    // Créer l'événement à envoyer
                    const evenement = {
                        id_contenu: etat.idContenu,
                        type_contenu: etat.typeContenu,
                        pourcentage_visibilite: etat.derniereVisibilite,
                        duree_exposition_ms: dureeExposition,
                        horodatage_debut: new Date(etat.horodatageDebut).toISOString(),
                        horodatage_fin: new Date(maintenant).toISOString()
                    };

                    CollecteurDonnees.ajouterEvenement(evenement);

                    // Réinitialiser l'état
                    etat.estVisible = false;
                    etat.horodatageDebut = null;
                    etat.derniereVisibilite = 0;
                }
            }
        });
    }

    /**
     * Envoie un heartbeat pour les contenus actuellement visibles.
     * Permet de ne pas perdre de données si l'utilisateur ferme l'onglet.
     */
    function envoyerHeartbeat() {
        const maintenant = Date.now();

        etatContenus.forEach(function (etat) {
            if (etat.estVisible && etat.horodatageDebut) {
                const dureeExposition = maintenant - etat.horodatageDebut;

                const evenement = {
                    id_contenu: etat.idContenu,
                    type_contenu: etat.typeContenu,
                    pourcentage_visibilite: etat.derniereVisibilite,
                    duree_exposition_ms: dureeExposition,
                    horodatage_debut: new Date(etat.horodatageDebut).toISOString(),
                    horodatage_fin: new Date(maintenant).toISOString()
                };

                CollecteurDonnees.ajouterEvenement(evenement);

                // Réinitialiser le chrono (pour ne pas compter deux fois)
                etat.horodatageDebut = maintenant;
            }
        });
    }

    /**
     * Initialise l'observateur et commence à surveiller les contenus.
     */
    function initialiser() {
        // Vérifier que l'API IntersectionObserver est disponible
        if (!('IntersectionObserver' in window)) {
            console.error('[CCC Tracking] IntersectionObserver non supporté');
            return;
        }

        // Créer l'observateur avec les seuils définis
        const observateur = new IntersectionObserver(
            gererChangementVisibilite,
            {
                root: null,        // viewport du navigateur
                rootMargin: '0px',
                threshold: SEUILS
            }
        );

        // Sélectionner tous les éléments avec l'attribut data-contenu-id
        const elements = document.querySelectorAll('[data-contenu-id]');
        elements.forEach(function (element) {
            observateur.observe(element);
        });

        console.log('[CCC Tracking] Observation démarrée pour', elements.length, 'contenus');

        // Heartbeat toutes les 5 secondes
        setInterval(envoyerHeartbeat, 5000);

        // Envoyer les données restantes avant fermeture
        // Note : on envoie le heartbeat mais on laisse le collecteur
        // gérer l'envoi via sendBeacon (seul mécanisme fiable dans beforeunload)
        window.addEventListener('beforeunload', function () {
            envoyerHeartbeat();
        });
    }

    return { initialiser };

})();

// Initialiser l'observateur au chargement du DOM
document.addEventListener('DOMContentLoaded', ObservateurVisibilite.initialiser);
