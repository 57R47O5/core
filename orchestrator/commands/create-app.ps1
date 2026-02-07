param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if (-not $Args -or $Args.Count -eq 0) {
    Write-Error "orc create-app: missing app name"
    exit 1
}

$appName = $Args[0]

# --------------------------------------------------
# Paths
# --------------------------------------------------
$OrcRoot  = Split-Path $PSScriptRoot -Parent
$RepoRoot = Split-Path $OrcRoot -Parent
$AppsRoot = Join-Path $RepoRoot "backend/apps"

if (-not (Test-Path $AppsRoot)) {
    Write-Error "backend/apps no existe en $RepoRoot"
    exit 1
}

# --------------------------------------------------
# Apps existentes
# --------------------------------------------------
$existingApps = Get-ChildItem `
    -Path $AppsRoot `
    -Directory `
    | Select-Object -ExpandProperty Name

if ($existingApps -contains $appName) {
    Write-Error "La app '$appName' ya existe en backend/apps"
    exit 1
}

# --------------------------------------------------
# Crear estructura
# --------------------------------------------------
$appRoot = Join-Path $AppsRoot $appName

$dirs = @(
    $appRoot,
    "$appRoot\models",
    "$appRoot\views",
    "$appRoot\urls",
    "$appRoot\serializers",
    "$appRoot\tests"
    "$appRoot\rest_controllers"
    "$appRoot\services"
    )
    
    foreach ($dir in $dirs) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    
    # --------------------------------------------------
    # Archivos base
    # --------------------------------------------------
    $files = @(
        "$appRoot\__init__.py",
        "$appRoot\models\__init__.py",
        "$appRoot\views\__init__.py",
        "$appRoot\urls\__init__.py",
        "$appRoot\serializers\__init__.py",
        "$appRoot\rest_controllers\__init__.py"
        "$appRoot\services\__init__.py"
        "$appRoot\tests\__init__.py"
        "$appRoot\permisos.py"
        "$appRoot\roles.py"
        "$appRoot\rest_urls.py"
)

foreach ($file in $files) {
    New-Item -ItemType File -Path $file | Out-Null
}

# apps.py
$appsPy = @"
from django.apps import AppConfig


class $(($appName.Substring(0,1).ToUpper() + $appName.Substring(1)))Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.$appName"
"@

$appsPy | Set-Content "$appRoot\apps.py"

# urls.py
$urlsPy = @"
from django.urls import path

urlpatterns = []
"@

$urlsPy | Set-Content "$appRoot\urls\urls.py"

Write-Host "App '$appName' creada en backend/apps/$appName"
