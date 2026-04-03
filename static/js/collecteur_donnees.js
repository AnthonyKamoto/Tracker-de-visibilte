/**
 * Module de collecte et d'envoi des données vers le serveur.
 * Gère la création de session, le tampon d'événements et l'envoi par lots.
 */

const CollecteurDonnees = (function () {

    // Identifiant unique de session (UUID v4)
    const idSession = crypto.randomUUID();

    // Tampon d'événements en attente d'envoi
    let tampon = [];

    // Taille maximale du tampon avant envoi automatique
    const TAILLE_MAX_TAMPON = 5;

    // Intervalle d'envoi automatique (3 secondes)
    const INTERVALLE_ENVOI_MS = 3000;

    // URL de base de l'API
    const URL_API = '';

    // Indicateur de session créée
    let sessionCreee = false;

    /**
     * Crée la session sur le serveur avec les informations contextuelles.
     */
    async function creerSession() {
        const contexte = InformationsContexte.collecter();
        const donnees = {
            id_session: idSession,
            ...contexte
        };

        try {
            const reponse = await fetch(URL_API + '/api/sessions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(donnees)
            });
            if (reponse.ok) {
                sessionCreee = true;
                console.log('[CCC Tracking] Session créée :', idSession);
            }
        } catch (erreur) {
            console.error('[CCC Tracking] Erreur création session :', erreur);
        }
    }

    /**
     * Ajoute un événement au tampon. Envoie le lot si le tampon est plein.
     */
    function ajouterEvenement(evenement) {
        tampon.push(evenement);
        if (tampon.length >= TAILLE_MAX_TAMPON) {
            envoyerLot();
        }
    }

    /**
     * Envoie le contenu du tampon au serveur via fetch.
     */
    async function envoyerLot() {
        if (tampon.length === 0) return;

        const evenementsAEnvoyer = [...tampon];
        tampon = [];

        const donnees = {
            id_session: idSession,
            evenements: evenementsAEnvoyer
        };

        try {
            await fetch(URL_API + '/api/evenements', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(donnees)
            });
            console.log('[CCC Tracking] Lot envoyé :', evenementsAEnvoyer.length, 'événements');
        } catch (erreur) {
            console.error('[CCC Tracking] Erreur envoi lot :', erreur);
            // Remettre les événements dans le tampon en cas d'échec
            tampon = evenementsAEnvoyer.concat(tampon);
        }
    }

    /**
     * Envoie les données restantes via sendBeacon (pour la fermeture de page).
     * sendBeacon est le seul mécanisme fiable dans beforeunload/visibilitychange.
     */
    function envoyerAvantFermeture() {
        if (tampon.length === 0) return;

        var succes = navigator.sendBeacon(
            URL_API + '/api/evenements',
            new Blob([JSON.stringify({
                id_session: idSession,
                evenements: tampon
            })], { type: 'application/json' })
        );

        if (succes) {
            console.log('[CCC Tracking] sendBeacon envoyé :', tampon.length, 'événements');
            tampon = [];
        }
    }

    /**
     * Initialise le collecteur : crée la session et lance l'envoi périodique.
     */
    function initialiser() {
        creerSession();

        // Envoi périodique toutes les 3 secondes
        setInterval(envoyerLot, INTERVALLE_ENVOI_MS);

        // Envoi des données restantes à la fermeture de la page
        window.addEventListener('beforeunload', envoyerAvantFermeture);

        // Envoi lorsque l'onglet devient masqué (changement d'onglet, alt-tab, etc.)
        document.addEventListener('visibilitychange', function () {
            if (document.visibilityState === 'hidden') {
                envoyerAvantFermeture();
            }
        });
    }

    return {
        initialiser,
        ajouterEvenement,
        envoyerLot,
        obtenirIdSession: function () { return idSession; }
    };

})();

// Initialiser le collecteur au chargement
CollecteurDonnees.initialiser();
