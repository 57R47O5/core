param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# --------------------------------------------------
# Paths
# --------------------------------------------------
$OrcRoot  = Split-Path $PSScriptRoot -Parent
$RepoRoot = Split-Path $OrcRoot -Parent
$AppsRoot = Join-Path $RepoRoot "backend/apps"

if (-not (Test-Path $AppsRoot)) {
    Write-Error "backend/apps no existe en $RepoRoot"
    exit 1
}

# --------------------------------------------------
# Listar apps
# --------------------------------------------------
$apps = Get-ChildItem `
    -Path $AppsRoot `
    -Directory `
    | Select-Object -ExpandProperty Name

if (-not $apps -or $apps.Count -eq 0) {
    Write-Host "(no hay apps instaladas)"
    exit 0
}

Write-Host "Apps disponibles:"
foreach ($app in $apps) {
    Write-Host " - $app"
}
