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

Write-Host "Destruyendo proyecto '$projectName'"

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
