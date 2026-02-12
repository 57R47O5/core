param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if ($Args.Count -eq 0) {
    Write-Host ""
    Write-Host "Uso:"
    Write-Host "  orc reset-db nombre_proyecto"
    Write-Host ""
    Write-Host "Descripción:"
    Write-Host "  Reaplica las migraciones Liquibase sin eliminar la base de datos."
    Write-Host ""
    return
}

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args

$liquibaseCmd = Join-Path $Context.OrcRoot "commands\liquibase.ps1"

Write-Host ""
Write-Host "[orc] Limpiando Liquibase CheckSums..."

& $liquibaseCmd `
    -Context $Context `
    -Args @("clearCheckSums")

if ($LASTEXITCODE -ne 0) {
    throw "[orc] Error limpiando Liquibase CheckSums"
}

Write-Host "[orc] Aplicando migraciones..."

& $liquibaseCmd `
    -Context $Context `
    -Args @("update")

if ($LASTEXITCODE -ne 0) {
    throw "[orc] Error aplicando migraciones"
}

Write-Host ""
Write-Host "[orc] Base actualizada correctamente."
Write-Host ""
