param (
    [Parameter(Mandatory = $true)]
    [string]$project,

    [Parameter(Mandatory = $true)]
    [string]$repoRoot
)

$backendPath  = Join-Path $repoRoot "backend\projects\$project"
$frontendPath = Join-Path $repoRoot "frontend\proyectos\$project"

if ((Test-Path $backendPath) -or (Test-Path $frontendPath)) {
    Write-Host "❌ El proyecto '$project' ya existe"
    exit 1
}

$helper = Join-Path $repoRoot "orchestrator\scripts\orc_create_project.py"

if (!(Test-Path $helper)) {
    Write-Host "❌ No se encontró el helper $helper"
    exit 1
}

Write-Host "🐗 Orc creando proyecto '$project' desde orc.yaml"
Write-Host ""

try {
    python $helper $project

    if ($LASTEXITCODE -ne 0) {
        throw "Error del generador"
    }
}
catch {
    Write-Host "❌ Error creando el proyecto '$project'"
    exit 1
}

Write-Host ""
Write-Host "✅ Proyecto '$project' creado correctamente"
Write-Host "Podés levantarlo con:"
Write-Host "  orc up $project"
