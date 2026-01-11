param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$RepoRoot = $Context.RepoRoot

if ($Args.Count -lt 1) {
    Write-Host "Uso:"
    Write-Host "  orc init-db <proyecto> [--local|--docker]"
    exit 1
}

$project = $Args[0]

Write-Host "🐗 Orc init-db"
Write-Host "Proyecto: $project"
Write-Host "DB Host: $($projectModel.Database.Host)"
Write-Host ""

. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\project-model.ps1"
. "$OrcRoot\lib\postgres-db.ps1"

$backendPath = $projectModel.Project.BackendPath

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
$projectModel | Format-List *
Write-Host "Llegamos hasta aqui"
Write-Host "libDir es $lbDir"

try {
    New-Item -ItemType Directory -Force -Path $lbDir | Out-Null
} catch {
    Write-Error "No se pudo preparar Liquibase runtime en $lbDir"
    exit 1
}

Ensure-PostgresDatabase -Context $Context

& "$OrcRoot\commands\liquibase.ps1" `
    -Context $Context `
    -Args    @("update")

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ init-db falló"
    exit 1
}

Write-Host ""
Write-Host "✅ Base de datos del proyecto '$project' inicializada correctamente"

