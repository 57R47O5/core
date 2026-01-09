param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$orcRoot  = $Context.OrcRoot
$repoRoot = $Context.RepoRoot
$project      = $projectModel.Project
$ProjectName  = $project.Name
$modo = $projectModel.Mode

Write-Host "Modo de ejecución: $modo"
Write-Host "Proyecto: $ProjectName"

# -------------------------
# Orc Project Model
# -------------------------
. "$OrcRoot\config\orc.config.ps1"
. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\env.ps1"
. "$OrcRoot\core\project-model.ps1"

# =========================
# MODO DOCKER
# =========================
if ($projectModel.Mode -eq "docker") {

    Write-Host "Levantando proyecto '$projectModel.Project' en modo DOCKER"

    $composePath = Join-Path $RepoRoot "docker"

    if (!(Test-Path $composePath)) {
        Write-Host "No se encontró el directorio docker en $composePath"
        exit 1
    }

    Push-Location $composePath

    docker compose up -d

    Pop-Location

    Write-Host ""
    Write-Host "Proyecto '$projectModel.Project' levantado (dockerizado)"
    exit 0
}

# =========================
# MODO LOCAL
# =========================

# ---- Backend ----
$backendPath  = $projectModel.Project.BackendPath
$FrontendPath = $projectModel.Project.FrontendPath
$PythonExe    = $projectModel.Backend.PythonExe
$venvActivate = $projectModel.Backend.ActivatePs
$managePy     = $projectModel.Backend.ManagePy

Write-Host $backendPath
if (!(Test-Path $backendPath)) {
    Write-Host "Backend del proyecto '$ProjectName' no existe"
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
    -ctx $Context

# ---- Levantar backend ----
Write-Host "Levantando backend ($ProjectName) en http://localhost:8000"

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
    Write-Host "Frontend del proyecto '$ProjectName' no existe"
    Write-Host "   Esperado en: $FrontendPath"
    exit 1
}

$packageJson = Join-Path $FrontendPath "package.json"
if (!(Test-Path $packageJson)) {
    Write-Host "No se encontró package.json en $FrontendPath"
    exit 1
}

Write-Host "Levantando frontend ($ProjectName) en http://localhost:3000"

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
Write-Host "Proyecto '$ProjectName' levantado (local)"
Write-Host "   Backend : http://localhost:8000"
Write-Host "   Frontend: http://localhost:3000"

exit 0
