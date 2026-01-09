param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$runtime  = $Context.Runtime
$orcRoot  = $Context.OrcRoot
$repoRoot = $Context.RepoRoot

Write-Host "Modo de ejecución: $runtime.Mode"
Write-Host "Proyecto: $runtime.Project"

# -------------------------
# Runtime Orc
# -------------------------
. "$OrcRoot\config\orc.config.ps1"
. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\env.ps1"
. "$OrcRoot\core\runtime.ps1"

# =========================
# MODO DOCKER
# =========================
if ($runtime.Mode -eq "docker") {

    Write-Host "Levantando proyecto '$runtime.Project' en modo DOCKER"

    $composePath = Join-Path $RepoRoot "docker"

    if (!(Test-Path $composePath)) {
        Write-Host "No se encontró el directorio docker en $composePath"
        exit 1
    }

    Push-Location $composePath

    docker compose up -d

    Pop-Location

    Write-Host ""
    Write-Host "Proyecto '$runtime.Project' levantado (dockerizado)"
    exit 0
}

# =========================
# MODO LOCAL
# =========================

# ---- Backend ----
$project      = $runtime.Project
$backendPath  = $runtime.Project.BackendPath
$FrontendPath = $runtime.Project.FrontendPath
$PythonExe    = $runtime.Backend.PythonExe
$venvActivate = $runtime.Backend.ActivatePs
$managePy     = $runtime.Backend.ManagePy

Write-Host $backendPath
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
    -ctx $Contex

# ---- Levantar backend ----
Write-Host "Levantando backend ($project) en http://localhost:8000"

Start-Process powershell `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "cd `"$backendPath`";
        Write-Host 'Activando venv...';
        . `"$venvActivate`";
        & `"$PythonExe`" manage.py runserver"
    ) `
    -WindowStyle Normal


# ---- Frontend ----

if (!(Test-Path $FrontendPath)) {
    Write-Host "Frontend del proyecto '$project' no existe"
    Write-Host "   Esperado en: $project.FrontendPath"
    exit 1
}

$packageJson = Join-Path $FrontendPath "package.json"
if (!(Test-Path $packageJson)) {
    Write-Host "No se encontró package.json en $project.FrontendPath"
    exit 1
}

Write-Host "Levantando frontend ($project) en http://localhost:3000"

Start-Process powershell `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "cd `"$FrontendPath`";
        Write-Host 'Ejecutando npm run dev...';
        npm run dev"
    ) `
    -WindowStyle Normal

Write-Host ""
Write-Host "Proyecto '$project' levantado (local)"
Write-Host "   Backend : http://localhost:8000"
Write-Host "   Frontend: http://localhost:3000"

exit 0
