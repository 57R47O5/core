param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if (-not $Args -or $Args.Count -lt 2) {
    Write-Error "Uso: orc remove-app <nombre_app> <nombre_proyecto>"
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
$orcAppsPath  = $ProjectModel.Project.AppsPath

if (-not (Test-Path $orcAppsPath)) {
    Write-Error "orc_apps.py no encontrado en $orcAppsPath"
    exit 1
}

# --------------------------------------------------
# Leer apps instaladas
# --------------------------------------------------
. "$OrcScriptRoot\core\orc-apps.ps1"

$appImport = "apps.$appName"
$installedApps = Get-OrcInstalledApps -ProjectModel $ProjectModel

if (-not ($installedApps -contains $appImport)) {
    Write-Error "La app '$appName' no está instalada en el proyecto"
    exit 1
}

# --------------------------------------------------
# Remover la app de ORC_APPS
# --------------------------------------------------
$appLinePattern = '^\s*"' + [regex]::Escape($appImport) + '"\s*,?\s*$'

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
        $insideBlock = $false
        $newLines += $line
        continue
    }

    if ($insideBlock -and $line -match $appLinePattern) {
        # 🔥 esta es la línea a eliminar → NO se agrega
        continue
    }

    $newLines += $line
}

Set-Content -Path $orcAppsPath -Value $newLines

Write-Host "App '$appName' removida del proyecto '$projectName'"
