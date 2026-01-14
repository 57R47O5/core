param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if (-not $Args -or $Args.Count -lt 2) {
    Write-Error "Uso: orc add-app <nombre_app> <nombre_proyecto>"
    exit 1
}

$appName     = $Args[0]
$projectName = $Args[1]

# --------------------------------------------------
# Contexto del proyecto (OBLIGATORIO)
# --------------------------------------------------
$OrcScriptRoot = Split-Path $PSScriptRoot -Parent
. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    @($projectName)

$ProjectModel = $Context.ProjectModel
$orcAppsPath  = $projectModel.Project.AppsPath

if (-not (Test-Path $orcAppsPath)) {
    Write-Error "orc_apps.py no encontrado en $orcAppsPath"
    exit 1
}

# --------------------------------------------------
# Verificar que la app exista en backend/apps
# --------------------------------------------------
$RepoRoot = $Context.RepoRoot
$appsRoot = Join-Path $RepoRoot "backend/apps"
$appPath  = Join-Path $appsRoot $appName

if (-not (Test-Path $appPath)) {
    Write-Error "La app '$appName' no existe en backend/apps"
    exit 1
}

# --------------------------------------------------
# Leer orc_apps.py
# --------------------------------------------------
. "$OrcScriptRoot\core\orc-apps.ps1"

$installedApps = Get-OrcInstalledApps -ProjectModel $ProjectModel

if ($installedApps -contains "apps.$appName") {
    Write-Error "La app '$appName' ya está instalada en el proyecto"
    exit 1
}

# --------------------------------------------------
# Insertar la app
# --------------------------------------------------
$content = Get-Content $orcAppsPath -Raw
$appImport = "apps.$appName"
$appLine = "    `"$appImport`","

Write-Host "appLine  es $appLine"

$lines = Get-Content $orcAppsPath

$insideBlock = $false
$newLines = @()

foreach ($line in $lines) {

    if ($line -match '^\s*ORC_APPS\s*=\s*\[') {
        $insideBlock = $true
        $newLines += $line
        continue
    }

    if ($insideBlock -and $line -match '^\s*\]') {
        # Insertamos ANTES del cierre
        $newLines += $appLine
        $newLines += $line
        $insideBlock = $false
        continue
    }

    $newLines += $line
}

Set-Content -Path $orcAppsPath -Value $newLines

Write-Host "App '$appName' agregada al proyecto '$projectName'"
