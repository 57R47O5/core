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

# --------------------------------------------------
# Paths base
# --------------------------------------------------
$OrcScriptRoot = $PSScriptRoot          # orchestrator/
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
. "$OrcScriptRoot\lib\orc-mode.ps1"
. "$OrcScriptRoot\core\context.ps1"
. "$OrcScriptRoot\core\runtime.ps1"

# --------------------------------------------------
# Resolver proyecto y modo
# --------------------------------------------------
$project = Resolve-OrcProject `
    -RepoRoot $RepoRoot `
    -Args     $rest

$mode = Resolve-OrcMode `
    -Args $rest

# --------------------------------------------------
# Construcción del runtime (UNA SOLA VEZ)
# --------------------------------------------------
$runtime = Resolve-OrcRuntime `
    -Mode        $mode `
    -ProjectName $project.Name `
    -RepoRoot    $RepoRoot `
    -OrcRoot     $OrcRoot

# --------------------------------------------------
# Contexto único
# --------------------------------------------------
$ctx = @{
    RepoRoot    = $RepoRoot
    OrcRoot     = $OrcRoot
    ProjectRoot = $project.Path
    Runtime     = $runtime
}

# --------------------------------------------------
# Dispatch
# --------------------------------------------------
$commandFile = Join-Path $OrcScriptRoot "commands\$command.ps1"

if (-not (Test-Path $commandFile)) {
    Write-Host "Comando no soportado: $command"
    exit 1
}

& $commandFile `
    -Context  $ctx `
    -Args     $rest

exit $LASTEXITCODE
