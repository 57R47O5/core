param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# --------------------------------------------------
# Validación mínima
# --------------------------------------------------
if (-not $Args -or $Args.Count -lt 2) {
    Write-Error "Uso: orc generate <modelo> <app>"
    exit 1
}

$modelName = $Args[0]
$appName   = $Args[1]

Write-Host "Orco generate → modelo: $modelName | app: $appName"

# --------------------------------------------------
# Invocación al generador Python (único responsable)
# --------------------------------------------------
python -m orchestrator.scripts.generators.generador $appName $modelName

if ($LASTEXITCODE -ne 0) {
    Write-Error "Error durante la generación"
    exit 1
}

Write-Host "Generación finalizada correctamente ✅"
exit 0
