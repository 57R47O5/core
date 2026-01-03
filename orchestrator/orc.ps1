param (
    [Parameter(Mandatory = $true)]
    [string]$command,
    
    [Parameter(Mandatory = $true)]
    [string]$project,

    [Parameter(Mandatory = $false)]
    [string]$target
    )
    
."$PSScriptRoot\lib\project-resolver.ps1"

$SupportedCommands = @(
    "up",
    "down",
    "reset",
    "status",
    "doctor"
)

$scriptRoot = $PSScriptRoot
$repoRoot   = Split-Path $scriptRoot -Parent

# -----------------------------
# Validación de comando
# -----------------------------
if (-not ($SupportedCommands -contains $command)) {
    Write-Host "Comando no soportado: $command"
    Write-Host ""
    Write-Host "Uso:"
    foreach ($cmd in $SupportedCommands) {
        Write-Host "  orc $cmd <proyecto>"
    }
    exit 1
}

if ($command -eq "reset" -and -not $target) {
    Write-Host "El comando 'reset' requiere un target"
    Write-Host "Uso: orc reset <proyecto> <frontend|backend>"
    exit 1
}

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

# =============================
# ORC DOWN
# =============================
if ($command -eq "down") {

    Write-Host "Deteniendo proyecto '$project'"

    # ---- Backend ----
    Write-Host "Deteniendo backend (manage.py runserver)"

    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -match "manage.py runserver"
        } |
        ForEach-Object {
            Write-Host "  ✖ Matando PID $($_.ProcessId)"
            Stop-Process -Id $_.ProcessId -Force
        }

    # ---- Frontend ----
    Write-Host "Deteniendo frontend (npm / vite)"

    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -match "npm run dev" -or
            $_.CommandLine -match "vite"
        } |
        ForEach-Object {
            Write-Host "  ✖ Matando PID $($_.ProcessId)"
            Stop-Process -Id $_.ProcessId -Force
        }

    Write-Host ""
    Write-Host "Proyecto '$project' detenido"

    exit 0
}

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

switch ($command) {
    "doctor" {
        . "$PSScriptRoot\commands\doctor.ps1"
        Invoke-OrcDoctor -Project $project
    }
}






