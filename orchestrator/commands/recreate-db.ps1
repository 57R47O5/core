param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if ($Args.Count -eq 0) {
    Write-Host ""
    Write-Host "Uso:"
    Write-Host "  orc recreate-db nombre_proyecto"
    Write-Host ""
    Write-Host "Descripción:"
    Write-Host "  Elimina la base de datos, la recrea y aplica migraciones."
    Write-Host ""
    return
}

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args

$OrcRoot = $Context.OrcRoot

. "$OrcRoot\lib\postgres-db.ps1"

Remove-PostgresDatabase -Context $Context

# if ($LASTEXITCODE -ne 0) {
#     throw "[orc] Error eliminando base de datos"
# }

Write-Host "[orc] Creando base de datos..."

Ensure-PostgresDatabase -Context $Context

# if ($LASTEXITCODE -ne 0) {
#     throw "[orc] Error creando base de datos"
# }

$liquibaseCmd = Join-Path $Context.OrcRoot "commands\liquibase.ps1"

Write-Host "[orc] Aplicando migraciones..."

& $liquibaseCmd `
    -Context $Context `
    -Args @("update")

    if ($LASTEXITCODE -ne 0) {
        throw "[orc] Error aplicando migraciones"
    }

Write-Host ""
Write-Host "[orc] Base recreada correctamente."
Write-Host ""
