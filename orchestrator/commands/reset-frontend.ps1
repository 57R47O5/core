# =============================
# ORC RESET FRONTEND <PROJECT>
# =============================

if ($command -eq "reset") {

    if ($target -ne "frontend") {
        Write-Host "Reset solo soporta 'frontend' por ahora"
        exit 1
    }

    $frontendPath = Join-Path $repoRoot "frontend\proyectos\$project"

    if (!(Test-Path $frontendPath)) {
        Write-Host "Frontend del proyecto '$project' no existe"
        exit 1
    }

    Write-Host "Reseteando frontend del proyecto '$project'"
    Write-Host "$frontendPath"

    $nodeModules = Join-Path $frontendPath "node_modules"
    $lockFile = Join-Path $frontendPath "package-lock.json"

    if (Test-Path $nodeModules) {
        Write-Host "Eliminando node_modules"
        Remove-Item -Recurse -Force $nodeModules
    }

    if (Test-Path $lockFile) {
        Write-Host "Eliminando package-lock.json"
        Remove-Item -Force $lockFile
    }

    Write-Host "Reinstalando dependencias"
    Push-Location $frontendPath
    npm install
    Pop-Location

    Write-Host "Frontend '$project' reseteado correctamente"
    exit 0
}

