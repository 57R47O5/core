param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$project  = $projectModel.Project
$projectName = $project.Name
$backendPath = $project.BackendPath
$FrontendPath = $project.FrontendPath

. "$OrcRoot\lib\postgres-db.ps1"

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

# Remove-PostgresDatabase -Context $Context

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
