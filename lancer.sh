#!/usr/bin/env bash
# Script de lancement des deux serveurs — macOS / Linux
# Usage : chmod +x lancer.sh && ./lancer.sh

echo ""
echo "========================================"
echo "  CCC — Tracker de visibilite"
echo "========================================"
echo ""

RACINE="$(cd "$(dirname "$0")" && pwd)"

# Activer le venv
if [ -f "$RACINE/venv/bin/activate" ]; then
    source "$RACINE/venv/bin/activate"
elif [ -f "$RACINE/venv/Scripts/activate" ]; then
    source "$RACINE/venv/Scripts/activate"
else
    echo "[ERREUR] Environnement virtuel introuvable."
    echo "Executez d'abord : python -m venv venv"
    exit 1
fi

# Fonction d'arret propre
arreter() {
    echo ""
    echo "Arret des serveurs..."
    kill "$PID_SERVEUR" "$PID_DASHBOARD" 2>/dev/null
    wait "$PID_SERVEUR" "$PID_DASHBOARD" 2>/dev/null
    echo "Serveurs arretes."
    exit 0
}

trap arreter INT TERM

# Lancer le serveur principal (port 5000)
echo "[1/2] Demarrage du serveur d'actualites (port 5000)..."
python "$RACINE/serveur/appli.py" &
PID_SERVEUR=$!

# Lancer le dashboard (port 5001)
echo "[2/2] Demarrage du dashboard (port 5001)..."
python "$RACINE/dashboard/appli.py" &
PID_DASHBOARD=$!

echo ""
echo "Les deux serveurs sont lances :"
echo "  Site d'actualites : http://localhost:5000"
echo "  Dashboard         : http://localhost:5001"
echo ""
echo "Appuyez sur Ctrl+C pour arreter les deux serveurs."
echo ""

# Attendre que l'un des deux s'arrete
while kill -0 "$PID_SERVEUR" 2>/dev/null && kill -0 "$PID_DASHBOARD" 2>/dev/null; do
    sleep 1
done
echo "[INFO] Un des serveurs s'est arrete."
arreter
