param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$runtime  = $Context.Runtime
$orcRoot  = $Context.OrcRoot
$repoRoot = $Context.RepoRoot
$project  = $runtime.Project

if ((Test-Path $project.BackendPath) -or (Test-Path $project.FrontendPath)) {
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

python $helper $project
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host "❌ El helper falló (exit code $exitCode)"
    exit 1
}

Write-Host ""
Write-Host "✅ Proyecto '$project' creado correctamente"
Write-Host "Podés levantarlo con:"
Write-Host "  orc up $project"
