# =============================
# ORC UP
# =============================
if ($command -eq "up") {

    # ---- Backend ----
    $backendPath  = Join-Path $repoRoot "backend\projects\$project"
    $venvActivate = Join-Path $backendPath ".venv\Scripts\activate.ps1"
    $managePy     = Join-Path $backendPath "manage.py"

    if (!(Test-Path $backendPath)) {
        Write-Host "Backend del proyecto '$project' no existe"
        exit 1
    }

    if (!(Test-Path $venvActivate)) {
        Write-Host "No se encontró el virtualenv en $venvActivate"
        exit 1
    }

    if (!(Test-Path $managePy)) {
        Write-Host "manage.py no encontrado en $backendPath"
        exit 1
    }

    # ---- Levantar backend ----
    Write-Host "Levantando backend ($project) en http://localhost:8000"

    $pythonExe = Join-Path $backendPath ".venv\Scripts\python.exe"

    Start-Process powershell `
        -ArgumentList @(
            "-NoExit",
            "-Command",
            "cd `"$backendPath`";
            Write-Host 'Activando venv...';
            . `"$venvActivate`";
            & `"$pythonExe`" manage.py runserver"
        ) `
        -WindowStyle Normal

    # ---- Frontend ----
    $frontendPath = Join-Path $repoRoot "frontend\proyectos\$project"

    if (!(Test-Path $frontendPath)) {
        Write-Host "Frontend del proyecto '$project' no existe"
        Write-Host "   Esperado en: $frontendPath"
        exit 1
    }

    # Validación mínima: vite.config.js o package.json
    $packageJson = Join-Path $frontendPath "package.json"
    if (!(Test-Path $packageJson)) {
        Write-Host "No se encontró package.json en $frontendPath"
        exit 1
    }

    Write-Host "Levantando frontend ($project) en http://localhost:3000"

    Start-Process powershell `
        -ArgumentList `
            "-NoExit",
            "-Command",
            "cd `"$frontendPath`"; Write-Host 'Ejecutando npm run dev...'; npm run dev" `
        -WindowStyle Normal


    Write-Host ""
    Write-Host "Proyecto '$project' levantado"
    Write-Host "   Backend : http://localhost:8000"
    Write-Host "   Frontend: http://localhost:3000"

    exit 0
}