param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args

$repoRoot     = $Context.RepoRoot
$projectModel = $Context.ProjectModel
$project      = $projectModel.Project
$ProjectName  = $project.Name
$OrcRoot      = $Context.OrcRoot

$orcPython = Join-Path $repoRoot "orchestrator\.venv\Scripts\python.exe"

if (!(Test-Path $orcPython)) {
    Write-Host "No se encontró el python del orco ($orcPython)"
    exit 1
}

Write-Host "Orc build '$ProjectName'"
Write-Host ""
$backendPath = $projectModel.Project.BackendPath

# ------------------------------------------------------------
# Db
# ------------------------------------------------------------

. "$OrcRoot\lib\postgres-db.ps1"
Ensure-PostgresDatabase -Context $Context


# ------------------------------------------------------------
# Backend (Django)
# ------------------------------------------------------------


if ($backendPath -and (Test-Path $backendPath)) {
    
Write-Host "Preparando backend ($backendPath)"

$venvPath = Join-Path $backendPath ".venv"
Write-Host "El entorno virtual está en $venvPath"

if (!(Test-Path $venvPath)) {
    Write-Host "Creando entorno virtual"
    & python3.14 -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error creando entorno virtual"
        exit 1
    }
} else {
    Write-Host "Entorno virtual ya existe"
}

$pip = Join-Path $venvPath "Scripts\pip.exe"
$requirements = Join-Path $backendPath "requirements.txt"

if (Test-Path $requirements) {
    Write-Host "Instalando dependencias Python"
    & $pip install -r $requirements
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error instalando dependencias Python"
        exit 1
    }
} else {
    Write-Host "No se encontró requirements.txt"
}
}


# ------------------------------------------------------------
# Frontend (build)
# ------------------------------------------------------------

# No instalamos FE

# --------------------------------------------------
# Liquibase (Fase 1 – local)
# --------------------------------------------------

Write-Host ""
Write-Host "[orc] Aplicando migraciones Liquibase"

$liquibaseCmd = Join-Path $Context.OrcRoot "commands\liquibase.ps1"

& $liquibaseCmd `
    -Context $Context `
    -Args @("clearCheckSums")
    
    if ($LASTEXITCODE -ne 0) {
        throw "[orc] Error limpiando Liquibase CheckSums"
    }

& $liquibaseCmd `
    -Context $Context `
    -Args @("update")
    
    if ($LASTEXITCODE -ne 0) {
        throw "[orc] Error aplicando migraciones Liquibase"
    }

# ------------------------------------------------------------
# Fin
# ------------------------------------------------------------

Write-Host ""
Write-Host "Build finalizado correctamente"
Write-Host "El proyecto está listo para:"
Write-Host "  orc up $ProjectName"
