param (
    # Contexto del orco
    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$OrcRoot,

    # Argumentos posicionales del comando
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# -------------------------
# Modo de ejecución
# -------------------------
$mode = "local"
if ($Args -contains "--docker") {
    $mode = "docker"
}

# Filtrar flags para obtener solo el nombre del proyecto
$filteredArgs = $Args | Where-Object { $_ -ne "--docker" }

if ($filteredArgs.Count -lt 1) {
    Write-Host "Falta el nombre del proyecto"
    Write-Host "   Uso: orc up <nombre-proyecto> [--docker]"
    exit 1
}

$project = $filteredArgs[0]

Write-Host "Modo de ejecución: $mode"
Write-Host "Proyecto: $project"
Write-Host ""

# -------------------------
# Runtime Orc
# -------------------------
. "$OrcRoot\config\orc.config.ps1"
. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\env.ps1"

$ctx = New-OrcContext `
    -RuntimeConfig $OrcRuntimeConfig `
    -ProjectConfig @{
        Name = $project
        Mode = $mode
    } `
    -Paths @{
        RepoRoot = $RepoRoot
        OrcRoot  = $OrcRoot
    }

# =========================
# MODO DOCKER
# =========================
if ($mode -eq "docker") {

    Write-Host "Levantando proyecto '$project' en modo DOCKER"

    $composePath = Join-Path $RepoRoot "docker"

    if (!(Test-Path $composePath)) {
        Write-Host "No se encontró el directorio docker en $composePath"
        exit 1
    }

    Push-Location $composePath

    docker compose up -d

    Pop-Location

    Write-Host ""
    Write-Host "Proyecto '$project' levantado (dockerizado)"
    exit 0
}

# =========================
# MODO LOCAL
# =========================

# ---- Backend ----
$backendPath  = Join-Path $RepoRoot "backend\projects\$project"
$venvActivate = Join-Path $backendPath ".venv\Scripts\activate.ps1"
$managePy     = Join-Path $backendPath "manage.py"
$pythonExe    = Join-Path $backendPath ".venv\Scripts\python.exe"

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

# ---- Env ----
New-OrcEnvFile `
    -ctx $ctx `
    -BackendPath $backendPath

# ---- Levantar backend ----
Write-Host "Levantando backend ($project) en http://localhost:8000"

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
$frontendPath = Join-Path $RepoRoot "frontend\proyectos\$project"

if (!(Test-Path $frontendPath)) {
    Write-Host "Frontend del proyecto '$project' no existe"
    Write-Host "   Esperado en: $frontendPath"
    exit 1
}

$packageJson = Join-Path $frontendPath "package.json"
if (!(Test-Path $packageJson)) {
    Write-Host "No se encontró package.json en $frontendPath"
    exit 1
}

Write-Host "Levantando frontend ($project) en http://localhost:3000"

Start-Process powershell `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "cd `"$frontendPath`";
        Write-Host 'Ejecutando npm run dev...';
        npm run dev"
    ) `
    -WindowStyle Normal

Write-Host ""
Write-Host "Proyecto '$project' levantado (local)"
Write-Host "   Backend : http://localhost:8000"
Write-Host "   Frontend: http://localhost:3000"

exit 0
