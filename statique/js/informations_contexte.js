/**
 * Module de détection des informations contextuelles.
 * Détecte le type d'appareil, le navigateur, la taille d'écran.
 */

const InformationsContexte = (function () {

    /**
     * Détecte le type d'appareil selon la largeur de l'écran.
     */
    function detecterTypeAppareil() {
        const largeur = window.innerWidth;
        if (largeur <= 768) return 'mobile';
        if (largeur <= 1024) return 'tablette';
        return 'ordinateur';
    }

    /**
     * Détecte le nom et la version du navigateur via userAgent.
     */
    function detecterNavigateur() {
        const ua = navigator.userAgent;

        if (ua.includes('Edg/')) {
            const version = ua.match(/Edg\/([\d.]+)/);
            return 'Edge ' + (version ? version[1] : '');
        }
        if (ua.includes('Chrome/') && !ua.includes('Edg/')) {
            const version = ua.match(/Chrome\/([\d.]+)/);
            return 'Chrome ' + (version ? version[1] : '');
        }
        if (ua.includes('Firefox/')) {
            const version = ua.match(/Firefox\/([\d.]+)/);
            return 'Firefox ' + (version ? version[1] : '');
        }
        if (ua.includes('Safari/') && !ua.includes('Chrome/')) {
            const version = ua.match(/Version\/([\d.]+)/);
            return 'Safari ' + (version ? version[1] : '');
        }

        return 'Autre';
    }

    /**
     * Collecte toutes les informations contextuelles de la session.
     */
    function collecter() {
        return {
            type_appareil: detecterTypeAppareil(),
            largeur_ecran: window.innerWidth,
            hauteur_ecran: window.innerHeight,
            navigateur: detecterNavigateur(),
            page_consultee: window.location.pathname
        };
    }

    return { collecter };

})();
