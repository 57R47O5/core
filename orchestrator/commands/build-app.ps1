param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# --------------------------------------------------
# Validación mínima
# --------------------------------------------------
if (-not $Args -or $Args.Count -lt 1) {
    Write-Error "Uso: orc build-app <app>"
    exit 1
}

$appName   = $Args[0]

Write-Host "Orco build-app →  app: $appName"

# --------------------------------------------------
# Invocación al compilador Python (único responsable)
# --------------------------------------------------
python -m orchestrator.scripts.build_app $appName

if ($LASTEXITCODE -ne 0) {
    Write-Error "Error durante el compilado de la app"
    exit 1
}

Write-Host "App compilada exitosamente ✅"
exit 0