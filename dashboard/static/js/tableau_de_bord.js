/**
 * Script du tableau de bord.
 * Appelle les API de statistiques et affiche les graphiques avec Chart.js.
 */

;(function () {
    var URL_API = window.URL_API || ""

    var graphiqueVisibilite = null
    var graphiqueDuree = null
    var graphiqueAppareils = null
    var graphiqueNavigateurs = null
    var graphiqueVues = null
    var intervalleAuto = null

    var COULEURS = [
        "#1a237e",
        "#283593",
        "#3949ab",
        "#5c6bc0",
        "#7986cb",
        "#9fa8da",
        "#c5cae9",
        "#e8eaf6",
    ]
    var COULEURS_VIVES = [
        "#ff6b35",
        "#00b4d8",
        "#2d6a4f",
        "#f7931e",
        "#0077b6",
        "#52b788",
        "#e63946",
        "#457b9d",
    ]

    // --- Indicateur de connexion ---
    function mettreAJourBadgeConnexion(connecte) {
        var badge = document.getElementById("badge-connexion")
        var texte = document.getElementById("badge-texte")
        if (connecte) {
            badge.className = "badge-connexion connecte"
            texte.textContent = "Serveur connecte"
        } else {
            badge.className = "badge-connexion deconnecte"
            texte.textContent = "Serveur injoignable"
        }
    }

    function obtenirParametresDate() {
        var dateDebut = document.getElementById("date-debut").value
        var dateFin = document.getElementById("date-fin").value
        var params = new URLSearchParams()
        if (dateDebut) params.append("date_debut", dateDebut)
        if (dateFin) params.append("date_fin", dateFin)
        var chaine = params.toString()
        return chaine ? "?" + chaine : ""
    }

    function formaterDuree(ms) {
        if (!ms || ms === 0) return "0 s"
        var secondes = ms / 1000
        if (secondes < 60) return secondes.toFixed(1) + " s"
        var minutes = Math.floor(secondes / 60)
        var reste = (secondes % 60).toFixed(0)
        return minutes + " min " + reste + " s"
    }

    function mettreAJourCartes(ds) {
        document.getElementById("val-sessions").textContent =
            ds.nombre_sessions || 0
        document.getElementById("val-evenements").textContent =
            ds.nombre_evenements || 0
        document.getElementById("val-duree").textContent = formaterDuree(
            ds.duree_moyenne_globale_ms,
        )
        document.getElementById("val-visibilite").textContent =
            ds.visibilite_moyenne_globale
                ? (ds.visibilite_moyenne_globale * 100).toFixed(0) + " %"
                : "- %"
    }

    function mettreAJourGraphiqueVisibilite(donnees) {
        var ctx = document
            .getElementById("graphique-visibilite")
            .getContext("2d")
        var etiquettes = donnees.map(function (d) {
            return d.id_contenu
        })
        var valeurs = donnees.map(function (d) {
            return (d.visibilite_moyenne * 100).toFixed(1)
        })
        if (graphiqueVisibilite) {
            graphiqueVisibilite.data.labels = etiquettes
            graphiqueVisibilite.data.datasets[0].data = valeurs
            graphiqueVisibilite.update()
            return
        }
        graphiqueVisibilite = new Chart(ctx, {
            type: "bar",
            data: {
                labels: etiquettes,
                datasets: [
                    {
                        label: "Visibilite moyenne (%)",
                        data: valeurs,
                        backgroundColor: COULEURS_VIVES,
                        borderRadius: 4,
                    },
                ],
            },
            options: {
                indexAxis: "y",
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        title: { display: true, text: "%" },
                    },
                },
            },
        })
    }

    function mettreAJourGraphiqueDuree(donnees) {
        var ctx = document.getElementById("graphique-duree").getContext("2d")
        var etiquettes = donnees.map(function (d) {
            return d.id_contenu
        })
        var valeurs = donnees.map(function (d) {
            return (d.duree_moyenne_ms / 1000).toFixed(1)
        })
        if (graphiqueDuree) {
            graphiqueDuree.data.labels = etiquettes
            graphiqueDuree.data.datasets[0].data = valeurs
            graphiqueDuree.update()
            return
        }
        graphiqueDuree = new Chart(ctx, {
            type: "bar",
            data: {
                labels: etiquettes,
                datasets: [
                    {
                        label: "Duree moyenne (s)",
                        data: valeurs,
                        backgroundColor: COULEURS,
                        borderRadius: 4,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: "Secondes" },
                    },
                },
            },
        })
    }

    function mettreAJourGraphiqueAppareils(donnees) {
        var ctx = document
            .getElementById("graphique-appareils")
            .getContext("2d")
        var etiquettes = donnees.map(function (d) {
            return d.type_appareil || "Inconnu"
        })
        var valeurs = donnees.map(function (d) {
            return d.nombre
        })
        if (graphiqueAppareils) {
            graphiqueAppareils.data.labels = etiquettes
            graphiqueAppareils.data.datasets[0].data = valeurs
            graphiqueAppareils.update()
            return
        }
        graphiqueAppareils = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: etiquettes,
                datasets: [
                    {
                        data: valeurs,
                        backgroundColor: COULEURS_VIVES.slice(
                            0,
                            etiquettes.length,
                        ),
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: { legend: { position: "bottom" } },
            },
        })
    }

    function mettreAJourGraphiqueNavigateurs(donnees) {
        var ctx = document
            .getElementById("graphique-navigateurs")
            .getContext("2d")
        var etiquettes = donnees.map(function (d) {
            return d.navigateur || "Inconnu"
        })
        var valeurs = donnees.map(function (d) {
            return d.nombre
        })
        if (graphiqueNavigateurs) {
            graphiqueNavigateurs.data.labels = etiquettes
            graphiqueNavigateurs.data.datasets[0].data = valeurs
            graphiqueNavigateurs.update()
            return
        }
        graphiqueNavigateurs = new Chart(ctx, {
            type: "pie",
            data: {
                labels: etiquettes,
                datasets: [
                    {
                        data: valeurs,
                        backgroundColor: COULEURS.slice(0, etiquettes.length),
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: { legend: { position: "bottom" } },
            },
        })
    }

    function mettreAJourGraphiqueVues(donnees) {
        var ctx = document.getElementById("graphique-vues").getContext("2d")
        var etiquettes = donnees.map(function (d) {
            return d.id_contenu
        })
        var valeurs = donnees.map(function (d) {
            return d.nombre_vues
        })
        if (graphiqueVues) {
            graphiqueVues.data.labels = etiquettes
            graphiqueVues.data.datasets[0].data = valeurs
            graphiqueVues.update()
            return
        }
        graphiqueVues = new Chart(ctx, {
            type: "bar",
            data: {
                labels: etiquettes,
                datasets: [
                    {
                        label: "Nombre de vues",
                        data: valeurs,
                        backgroundColor: "#1a237e",
                        borderRadius: 4,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: "Vues" },
                    },
                },
            },
        })
    }

    function mettreAJourTableau(donnees) {
        var corps = document.getElementById("corps-tableau")
        if (!donnees || donnees.length === 0) {
            corps.innerHTML =
                '<tr><td colspan="5">' +
                '<div class="etat-vide-conteneur">' +
                '<i class="fa-solid fa-chart-column etat-vide-icone"></i>' +
                '<div class="etat-vide-titre">Aucune donnee pour le moment</div>' +
                '<div class="etat-vide-texte">Naviguez sur le site d\'actualites pour generer des donnees de visibilite. Les statistiques apparaitront ici automatiquement.</div>' +
                '<a href="' + URL_API + '/actualites" class="etat-vide-lien" target="_blank"><i class="fa-solid fa-arrow-right"></i> Ouvrir le site</a>' +
                '</div>' +
                '</td></tr>'
            return
        }
        corps.innerHTML = donnees
            .map(function (d) {
                return (
                    "<tr><td>" +
                    d.id_contenu +
                    "</td><td>" +
                    (d.type_contenu || "-") +
                    "</td><td>" +
                    d.nombre_vues +
                    "</td><td>" +
                    (d.duree_moyenne_ms / 1000).toFixed(1) +
                    "</td><td>" +
                    (d.visibilite_moyenne * 100).toFixed(0) +
                    " %</td></tr>"
                )
            })
            .join("")
    }

    async function chargerDonnees() {
        var params = obtenirParametresDate()
        try {
            var resultats = await Promise.all([
                fetch(URL_API + "/api/statistiques/contenus" + params).then(
                    function (r) {
                        return r.json()
                    },
                ),
                fetch(URL_API + "/api/statistiques/sessions" + params).then(
                    function (r) {
                        return r.json()
                    },
                ),
                fetch(URL_API + "/api/statistiques/appareils" + params).then(
                    function (r) {
                        return r.json()
                    },
                ),
                fetch(URL_API + "/api/statistiques/navigateurs" + params).then(
                    function (r) {
                        return r.json()
                    },
                ),
            ])
            var repContenus = resultats[0]
            var repSessions = resultats[1]
            var repAppareils = resultats[2]
            var repNavigateurs = resultats[3]

            mettreAJourBadgeConnexion(true)

            if (repSessions.succes) mettreAJourCartes(repSessions.donnees)
            if (repContenus.succes && repContenus.donnees.length > 0) {
                mettreAJourGraphiqueVisibilite(repContenus.donnees)
                mettreAJourGraphiqueDuree(repContenus.donnees)
                mettreAJourGraphiqueVues(repContenus.donnees)
                mettreAJourTableau(repContenus.donnees)
            } else {
                mettreAJourTableau([])
            }
            if (repAppareils.succes && repAppareils.donnees.length > 0)
                mettreAJourGraphiqueAppareils(repAppareils.donnees)
            if (repNavigateurs.succes && repNavigateurs.donnees.length > 0)
                mettreAJourGraphiqueNavigateurs(repNavigateurs.donnees)
        } catch (erreur) {
            console.error("[CCC Dashboard] Erreur :", erreur)
            mettreAJourBadgeConnexion(false)
            mettreAJourTableau([])
        }
    }

    // --- Rafraichissement automatique ---
    var toggleRefresh = document.getElementById("toggle-refresh")
    if (toggleRefresh) {
        toggleRefresh.addEventListener("change", function () {
            if (this.checked) {
                chargerDonnees()
                intervalleAuto = setInterval(chargerDonnees, 10000)
            } else {
                if (intervalleAuto) {
                    clearInterval(intervalleAuto)
                    intervalleAuto = null
                }
            }
        })
    }

    document
        .getElementById("btn-actualiser")
        .addEventListener("click", chargerDonnees)
    chargerDonnees()
})()
