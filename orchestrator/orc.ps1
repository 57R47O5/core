param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if ($Args.Count -eq 0) {
    Write-Host "orc: no command provided"
    exit 1
}

$command = $Args[0]
$rest    = if ($Args.Count -gt 1) { $Args[1..($Args.Count - 1)] } else { @() }

$OrcScriptRoot = $PSScriptRoot

# --------------------------------------------------
# Dispatch
# --------------------------------------------------
$commandFile = Join-Path $OrcScriptRoot "commands\$command.ps1"

if (-not (Test-Path $commandFile)) {

    if ($command -like "*-*") {
        $group = $command.Split('-')[0]
        $grouped = Join-Path $OrcScriptRoot "commands\$group\$command.ps1"

        if (Test-Path $grouped) {
            $commandFile = $grouped
        }
        else {
            Write-Host "Comando no soportado: $command"
            exit 1
        }
    }
    else {
        Write-Host "Comando no soportado: $command"
        exit 1
    }
}

# --------------------------------------------------
# Contexto (si el comando lo requiere)
# --------------------------------------------------
. "$OrcScriptRoot\core\contextualizer.ps1"

& $commandFile `
    -Args    $rest

exit $LASTEXITCODE
