param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if ($Args.Count -eq 0) {
    Write-Host "orc: no command provided"
    exit 1
}

$command = $Args[0]
$rest    = $Args[1..($Args.Count - 1)]

# --------------------------------------------------
# Paths base (NO usar Get-Location)
# --------------------------------------------------
$OrcScriptRoot = $PSScriptRoot               # orchestrator/
$OrcRoot       = $OrcScriptRoot              
$RepoRoot      = Split-Path $OrcRoot -Parent
$OrcDataRoot   = Join-Path $OrcRoot ".orc"

if (-not (Test-Path $OrcRoot)) {
    throw "OrcRoot no encontrado en $OrcRoot"
}

# --------------------------------------------------
# Load core libs
# --------------------------------------------------
. "$OrcScriptRoot\lib\project-resolver.ps1"
. "$OrcScriptRoot\lib\librarian.ps1"

# --------------------------------------------------
# Supported commands
# --------------------------------------------------
$commandFile = Join-Path $OrcScriptRoot "commands\$command.ps1"

if (-not (Test-Path $commandFile)) {
    Write-Host "Comando no soportado: $command"
    exit 1
}

# --------------------------------------------------
# Dispatch
# --------------------------------------------------
& $commandFile `
    -RepoRoot $RepoRoot `
    -OrcRoot  $OrcRoot `
    -Args     $rest

exit $LASTEXITCODE
