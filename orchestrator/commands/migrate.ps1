param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args

$projectModel = $Context.ProjectModel
$OrcRoot = $Context.OrcRoot
$project      = $projectModel.Project
$projectName  = $project.Name
$backendPath = $projectModel.Project.BackendPath

Write-Host ""
Write-Host "Orco migrate - Fase 1 (descubrimiento)" -ForegroundColor Cyan
Write-Host "Proyecto: $projectName"
Write-Host ""

$orcAppsPath = Join-Path $backendPath "config\settings\orc_apps.py"
if (-not (Test-Path $orcAppsPath)) {
    throw "No se encontró settings/orc_apps.py"
}

Write-Host "Apps del orco detectadas:" -ForegroundColor Yellow

$apps = python `
"$OrcScriptRoot\scripts\inspect_orc_apps.py" `
$orcAppsPath

Write-Host "las apps son $apps"
foreach ($app in $apps) {
    Write-Host " - $app"
}

Write-Host ""
Write-Host "Modelos migrables por app:" -ForegroundColor Yellow

foreach ($app in $apps) {
    
    Write-Host ""
    Write-Host "${app}:" -ForegroundColor Cyan   
    
    
    $models = python `
    "$OrcScriptRoot\scripts\inspect_app_models.py" `
    $app
    
    if ($models.Count -eq 0) {
        Write-Host "  (sin modelos migrables)" -ForegroundColor DarkGray
        continue
    }
    
    foreach ($model in $models) {
        Write-Host "  - $model"
    }
}