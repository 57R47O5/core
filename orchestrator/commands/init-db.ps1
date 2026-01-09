param (
    # Contexto del orco
    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$OrcRoot,

    # Argumentos posicionales
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$project = Resolve-OrcProject `
    -RepoRoot $RepoRoot `
    -Args     $Args `
    -Required

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
. "$OrcRoot\core\runtime.ps1"

$backendPath = Join-Path $RepoRoot "backend\projects\$project"

if (-not (Test-Path $backendPath)) {
    Write-Error "❌ El proyecto '$project' no existe (backend no encontrado)"
    exit 1
}

$runtime = Resolve-OrcRuntime `
    -Mode        $mode `
    -ProjectName $project `
    -RepoRoot    $RepoRoot `
    -OrcRoot     $OrcRoot

if (-not $runtime.Liquibase) {
    Write-Error "[orc] Runtime no define configuración de Liquibase"
    exit 1
}

Write-Host "🐗 Inicializando base de datos con Liquibase"
Write-Host ""

$lbDir = $runtime.Liquibase.WorkDir

try {
    New-Item -ItemType Directory -Force -Path $lbDir | Out-Null
} catch {
    Write-Error "❌ No se pudo preparar Liquibase runtime en $lbDir"
    exit 1
}

& "$OrcRoot\commands\liquibase.ps1" `
    -Args @("update") `
    -RepoRoot $RepoRoot `
    -LiquibaseRuntime $runtime.Liquibase.WorkDir

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ init-db falló"
    exit 1
}

Write-Host ""
Write-Host "✅ Base de datos del proyecto '$project' inicializada correctamente"

