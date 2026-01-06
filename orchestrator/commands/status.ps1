if ($command -eq "status") {

    Write-Host ""
    Write-Host "ORC STATUS - $project"
    Write-Host ""

    # ---------- Backend ----------
    $backendPath = Join-Path $repoRoot "backendpy\projects\$project"
    $managePy = Join-Path $backendPath "manage.py"
    $venvPath = Join-Path $backendPath ".venv"

    Write-Host "Backend:"

    if (Test-Path $backendPath) {
        Write-Host "  Proyecto encontrado"
    } else {
        Write-Host "  Proyecto NO existe"
    }

    if (Test-Path $managePy) {
        Write-Host "  manage.py presente"
    } else {
        Write-Host "  manage.py ausente"
    }

    if (Test-Path $venvPath) {
        Write-Host "  Virtualenv presente"
    } else {
        Write-Host "  Virtualenv ausente"
    }

    # Django corriendo?
    $djangoRunning = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if ($djangoRunning) {
        Write-Host "  Django corriendo en http://localhost:8000"
    } else {
        Write-Host "  Django NO esta corriendo"
    }

    Write-Host ""

    # ---------- Frontend ----------
    $frontendPath = Join-Path $repoRoot "frontend\proyectos\$project"

    Write-Host "Frontend:"

    if (Test-Path $frontendPath) {
        Write-Host "  Proyecto frontend encontrado"
    } else {
        Write-Host "  Proyecto frontend NO existe"
    }

    # Vite (puerto 3000 o 5173)
    $vite3000 = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
    $vite5173 = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue

    if ($vite3000) {
        Write-Host "  Vite corriendo en http://localhost:3000"
    }
    elseif ($vite5173) {
        Write-Host "  Vite corriendo en http://localhost:5173"
    }
    else {
        Write-Host "  Vite NO esta corriendo"
    }

    Write-Host ""

    # ---------- Estado general ----------
    Write-Host "Estado general:"

    if ($djangoRunning -and ($vite3000 -or $vite5173)) {
        Write-Host "  Proyecto operativo"
    }
    elseif ($djangoRunning -or ($vite3000 -or $vite5173)) {
        Write-Host "  Proyecto parcialmente levantado"
    }
    else {
        Write-Host "  Proyecto detenido"
    }

    Write-Host ""
    exit 0
}