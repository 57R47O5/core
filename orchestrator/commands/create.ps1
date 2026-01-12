param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$repoRoot = $Context.RepoRoot
$project  = $projectModel.Project
$ProjectName  = $project.Name

$orcPython = "$RepoRoot\orchestrator\.venv\Scripts\python.exe"

$conflicts = @()

if ($project.BackendPath -and (Test-Path $project.BackendPath)) {
    $conflicts += "backend"
}

if ($project.FrontendPath -and (Test-Path $project.FrontendPath)) {
    $conflicts += "frontend"
}

if ($conflicts.Count -gt 0) {
    Write-Host "❌ El proyecto '$ProjectName' ya existe ($($conflicts -join ', '))"
    exit 1
}

$helper = Join-Path $repoRoot "orchestrator\scripts\orc_create_project.py"

if (!(Test-Path $helper)) {
    Write-Host "❌ No se encontró el helper $helper"
    exit 1
}

Write-Host "🐗 Orc creando proyecto '$ProjectName' desde orc.yaml"
Write-Host ""

& $orcPython orchestrator/scripts/orc_create_project.py $ProjectName
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host "❌ El helper falló (exit code $exitCode)"
    exit 1
}

Write-Host ""
Write-Host "✅ Proyecto '$ProjectName' creado correctamente"
Write-Host "Podés levantarlo con:"
Write-Host "  orc up $ProjectName"
