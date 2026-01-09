param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$orcRoot  = $Context.OrcRoot
$repoRoot = $Context.RepoRoot

if ($Args.Count -lt 1) {
    Write-Host "Uso:"
    Write-Host "  orc init-db <proyecto> [--local|--docker]"
    exit 1
}

$project = $Args[0]
$mode    = "docker"

if ($Args -contains "--local")  { $mode = "local"  }
if ($Args -contains "--docker") { $mode = "docker" }

Write-Host "🐗 Orc init-db"
Write-Host "Proyecto: $project"
Write-Host "Modo: $mode"
Write-Host ""

. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\project-model.ps1"

$backendPath = Join-Path $RepoRoot "backend\projects\$project"

if (-not (Test-Path $backendPath)) {
    Write-Error "❌ El proyecto '$project' no existe (backend no encontrado)"
    exit 1
}

if (-not $projectModel.Liquibase) {
    Write-Error "[orc] El modelo del proyecto no define configuración de Liquibase"
    exit 1
}

Write-Host "🐗 Inicializando base de datos con Liquibase"
Write-Host ""

$lbDir = $projectModel.Liquibase.WorkDir

try {
    New-Item -ItemType Directory -Force -Path $lbDir | Out-Null
} catch {
    Write-Error "❌ No se pudo preparar Liquibase runtime en $lbDir"
    exit 1
}

& "$OrcRoot\commands\liquibase.ps1" `
    -Args @("update") `
    -RepoRoot $RepoRoot `
    -LiquibaseRuntime $projectModel.Liquibase.WorkDir

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ init-db falló"
    exit 1
}

Write-Host ""
Write-Host "✅ Base de datos del proyecto '$project' inicializada correctamente"

