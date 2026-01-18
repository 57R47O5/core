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
$frontendPath = $projectModel.Project.FrontendPath
$frontendBaseDir = Resolve-Path (
    Join-Path $frontendPath "..\.."
)

Write-Host ""
Write-Host "Ejecutando motor de migraciones:" -ForegroundColor Yellow

$output = python `
"$OrcScriptRoot\scripts\migrate_engine.py" `
$projectName 

foreach ($line in $output) {
    Write-Host "[migrate] $line"
}

