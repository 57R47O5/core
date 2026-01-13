param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$repoRoot     = $Context.RepoRoot
$projectModel = $Context.ProjectModel
$project      = $projectModel.Project
$ProjectName  = $project.Name

$orcPython = Join-Path $repoRoot "orchestrator\.venv\Scripts\python.exe"

if (!(Test-Path $orcPython)) {
    Write-Host "No se encontró el python del orco ($orcPython)"
    exit 1
}

Write-Host "Orc build '$ProjectName'"
Write-Host ""



# ------------------------------------------------------------
# Db
# ------------------------------------------------------------

. "$OrcRoot\lib\postgres-db.ps1"
Ensure-PostgresDatabase -Context $Context

# ------------------------------------------------------------
# Backend (Django)
# ------------------------------------------------------------

$backendPath = $projectModel.Project.BackendPath
$frontendPath = $projectModel.Project.FrontendPath

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

if ($frontendPath -and (Test-Path $frontendPath)) {

    Write-Host "Construyendo frontend ($frontendPath)"

    Push-Location $frontendPath

    $hasPackageJson = Test-Path "package.json"

    if (-not $hasPackageJson) {

        Write-Host "Inicializando frontend con Vite (React)"

        $env:CI = "true"

        npx.cmd create-vite . --template react --yes
        if ($LASTEXITCODE -ne 0) {
            Pop-Location
            throw "Error creando proyecto Vite"
        }

        npm.cmd install
        if ($LASTEXITCODE -ne 0) {
            Pop-Location
            throw "Error ejecutando npm install"
        }

        Patch-ViteConfig -ProjectDir $frontendPath

    }
    else {

        Write-Host "Frontend ya inicializado - instalando dependencias"

        npm.cmd install
        if ($LASTEXITCODE -ne 0) {
            Pop-Location
            throw "Error ejecutando npm install"
        }
    }

    Pop-Location
}
else {
    Write-Host "Frontend no configurado para este proyecto"
}


# ------------------------------------------------------------
# Fin
# ------------------------------------------------------------

Write-Host ""
Write-Host "Build finalizado correctamente"
Write-Host "El proyecto está listo para:"
Write-Host "  orc up $ProjectName"
