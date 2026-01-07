param (
    # Contexto del orco
    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$OrcRoot,

    # Argumentos posicionales del comando
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if ($Args.Count -lt 1) {
    Write-Host "Falta el nombre del proyecto"
    Write-Host "   Uso: orc destroy <nombre-proyecto>"
    exit 1
}

$project = $Args[0]

$backendPath   = Join-Path $repoRoot "backend\projects\$project"
$frontendPath  = Join-Path $repoRoot "frontend\proyectos\$project"
$liquibasePath = Join-Path $repoRoot "docker\liquibase\changelog\projects\$project"

Write-Host "Destruyendo proyecto '$project'"

if (Test-Path $backendPath) {
    Write-Host "Eliminando backend..."
    Remove-Item -Recurse -Force $backendPath
}

if (Test-Path $frontendPath) {
    Write-Host "Eliminando frontend..."
    Remove-Item -Recurse -Force $frontendPath
}

if (Test-Path $liquibasePath) {
    Write-Host "Eliminando configuración Liquibase..."
    Remove-Item -Recurse -Force $liquibasePath
}

Write-Host ""
Write-Host "Proyecto '$project' destruido"

exit 0
