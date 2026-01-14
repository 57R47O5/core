param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args

$projectModel  = $Context.ProjectModel
$project  = $projectModel.Project
$projectName = $project.Name
$backendPath = $project.BackendPath
$FrontendPath = $project.FrontendPath


Write-Host "Destruyendo proyecto '$projectName'"

$db = $projectModel.Database

Write-Host ""
Write-Host "⚠️  DESTRUCTIVE OPERATION"
Write-Host ""
Write-Host "Project:  $projectName"
Write-Host "Database: $($db.Name)"
Write-Host ""

$confirmation = Read-Host "Type the database name to confirm"

if ($confirmation -ne $db.Name) {
    Write-Host "❌ Confirmación incorrecta. Operación cancelada."
    exit 1
}

$OrcRoot = $Context.OrcRoot
. "$OrcRoot\lib\postgres-db.ps1"
if (-not (Get-Command Remove-PostgresDatabase -ErrorAction SilentlyContinue)) {
    throw "Remove-PostgresDatabase NO fue cargada (postgres-db.ps1)"
}
Remove-PostgresDatabase -Context $Context

if (Test-Path $backendPath) {
    Write-Host "Eliminando backend..."
    Remove-Item -Recurse -Force $backendPath
}

if (Test-Path $frontendPath) {
    Write-Host "Eliminando frontend..."
    Remove-Item -Recurse -Force $frontendPath
}

if (Test-Path $project.LiquibasePath) {
    Write-Host "Eliminando configuración Liquibase..."
    Remove-Item -Recurse -Force $project.LiquibasePath
}

Write-Host ""
Write-Host "Proyecto '$projectName' destruido"

exit 0
