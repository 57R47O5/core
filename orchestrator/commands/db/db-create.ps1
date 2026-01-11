param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# --------------------------------------------------
# Contexto
# --------------------------------------------------
. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\project-model.ps1"
. "$OrcRoot\lib\postgres-db.ps1"

$projectModel = $Context.ProjectModel

Write-Host "Orc db-create"
Write-Host "Proyecto: $($projectModel.Project.Name)"
Write-Host ""

# --------------------------------------------------
# Validaciones
# --------------------------------------------------
if (-not $projectModel.Database) {
    Write-Error "[orc] El proyecto no define Database en el project model"
    exit 1
}

if (-not $projectModel.Liquibase) {
    Write-Error "[orc] El proyecto no define configuración de Liquibase"
    exit 1
}

# --------------------------------------------------
# Crear base de datos (idempotente)
# --------------------------------------------------
Write-Host "Creando base de datos (si no existe)"
Ensure-PostgresDatabase -Context $Context

# --------------------------------------------------
# Ejecutar Liquibase (dockerizado)
# --------------------------------------------------
Write-Host ""
Write-Host "Aplicando migraciones con Liquibase"

& "$OrcRoot\commands\liquibase.ps1" `
    -Context $Context `
    -Args @("update")

if ($LASTEXITCODE -ne 0) {
    Write-Error "db-create falló durante liquibase update"
    exit 1
}

Write-Host ""
Write-Host "Base de datos '$($projectModel.Database.Name)' creada e inicializada"
