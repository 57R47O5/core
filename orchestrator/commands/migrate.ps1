param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args
    
$projectModel = $Context.ProjectModel
$project      = $projectModel.Project
$projectName  = $project.Name

Write-Host ""
Write-Host "Ejecutando motor de migraciones:" -ForegroundColor Yellow

$output = python `
"$OrcScriptRoot\scripts\migrate_engine.py" `
$projectName 

foreach ($line in $output) {
    Write-Host "[migrate] $line"
}

