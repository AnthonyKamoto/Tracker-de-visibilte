# Script de lancement des deux serveurs — Windows (PowerShell)
# Usage : .\lancer.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CCC — Tracker de visibilite"          -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activer le venv
$racine = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvActivate = Join-Path $racine "venv\Scripts\Activate.ps1"

if (-Not (Test-Path $venvActivate)) {
    Write-Host "[ERREUR] Environnement virtuel introuvable." -ForegroundColor Red
    Write-Host "Executez d'abord : python -m venv venv" -ForegroundColor Yellow
    exit 1
}

& $venvActivate

# Lancer le serveur principal (port 5000)
Write-Host "[1/2] Demarrage du serveur d'actualites (port 5000)..." -ForegroundColor Green
$serveur = Start-Process -FilePath "python" `
    -ArgumentList "serveur/appli.py" `
    -WorkingDirectory $racine `
    -PassThru -NoNewWindow

# Lancer le dashboard (port 5001)
Write-Host "[2/2] Demarrage du dashboard (port 5001)..." -ForegroundColor Green
$dashboard = Start-Process -FilePath "python" `
    -ArgumentList "dashboard/appli.py" `
    -WorkingDirectory $racine `
    -PassThru -NoNewWindow

Write-Host ""
Write-Host "Les deux serveurs sont lances :" -ForegroundColor Cyan
Write-Host "  Site d'actualites : http://localhost:5000" -ForegroundColor White
Write-Host "  Dashboard         : http://localhost:5001" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arreter les deux serveurs." -ForegroundColor Yellow
Write-Host ""

# Attendre et gerer l'arret propre
try {
    while ($true) {
        if ($serveur.HasExited -or $dashboard.HasExited) {
            Write-Host "[INFO] Un des serveurs s'est arrete." -ForegroundColor Yellow
            break
        }
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Host "Arret des serveurs..." -ForegroundColor Yellow
    if (-Not $serveur.HasExited) { Stop-Process -Id $serveur.Id -Force -ErrorAction SilentlyContinue }
    if (-Not $dashboard.HasExited) { Stop-Process -Id $dashboard.Id -Force -ErrorAction SilentlyContinue }
    Write-Host "Serveurs arretes." -ForegroundColor Green
}
