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
$projectName = if (-not $rest -or $rest.Count -eq 0) {
    $null
}
elseif ($rest -is [array]) {
    $rest[0]
}
else {
    $rest
}

# --------------------------------------------------
# Paths base
# --------------------------------------------------
$OrcScriptRoot = $PSScriptRoot          # orchestrator/
$OrcRoot       = $OrcScriptRoot
$RepoRoot      = Split-Path $OrcRoot -Parent

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
. "$OrcScriptRoot\core\project-model.ps1"

# --------------------------------------------------
# Resolver  modo
# --------------------------------------------------

$mode = Resolve-OrcMode -Args $rest


# --------------------------------------------------
# El orco identifica si el comando se aplica a  un proyecto
# preexistente
# --------------------------------------------------

$projectRequired = switch ($command) {
    "create"  { $false }
    default   { $true }
}

# --------------------------------------------------
# Construcción del modelo de proyecto (UNA SOLA VEZ)
# --------------------------------------------------
$projectModel = Resolve-ProjectModel `
    -Mode        $mode `
    -ProjectName $projectName `
    -RepoRoot    $RepoRoot `
    -OrcRoot     $OrcRoot `
    -ProjectRequired $projectRequired

# --------------------------------------------------
# Contexto único
# --------------------------------------------------
$ctx = @{
    RepoRoot    = $RepoRoot
    OrcRoot     = $OrcRoot
    ProjectModel= $projectModel
    Docker       = @{
        NetworkName = "orc-$($projectModel.Project.Name)"
    }
}

# --------------------------------------------------
# Dispatch
# --------------------------------------------------
# 1) Intentar comando plano: commands/up.ps1
$commandFile = Join-Path $OrcScriptRoot "commands\$command.ps1"

if (-not (Test-Path $commandFile)) {

    # 2) Intentar comando jerárquico: commands/db/db-create.ps1
    if ($command -like "*-*") {
        $group = $command.Split('-')[0]
        $groupedCommandFile = Join-Path $OrcScriptRoot "commands\$group\$command.ps1"

        if (Test-Path $groupedCommandFile) {
            $commandFile = $groupedCommandFile
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

& $commandFile `
    -Context  $ctx `
    -Args     $rest

exit $LASTEXITCODE
