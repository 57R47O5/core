function Resolve-OrcContext {
    param (
        [Parameter(Mandatory)]
        [bool]$Required,

        [string[]]$Args
    )

    # --------------------------------------------------
    # Paths base
    # --------------------------------------------------
    $OrcRoot  = $PSScriptRoot | Split-Path -Parent
    $RepoRoot = Split-Path $OrcRoot -Parent

    if (-not (Test-Path $OrcRoot)) {
        throw "OrcRoot no encontrado en $OrcRoot"
    }

    # --------------------------------------------------
    # Load core libs
    # --------------------------------------------------
    . "$OrcRoot\lib\project-resolver.ps1"
    . "$OrcRoot\lib\librarian.ps1"
    . "$OrcRoot\lib\orc-mode.ps1"
    . "$OrcRoot\core\context.ps1"
    . "$OrcRoot\core\project-model.ps1"

    # --------------------------------------------------
    # Parsing semántico
    # --------------------------------------------------
    $projectName = if (-not $Args -or $Args.Count -eq 0) {
        $null
    }
    elseif ($Args -is [array]) {
        $Args[0]
    }
    else {
        $Args
    }

    # --------------------------------------------------
    # Resolver modo
    # --------------------------------------------------
    $mode = Resolve-OrcMode -Args $Args

    # --------------------------------------------------
    # Construcción del modelo de proyecto
    # --------------------------------------------------
    $projectModel = Resolve-ProjectModel `
        -Mode            $mode `
        -ProjectName     $projectName `
        -RepoRoot        $RepoRoot `
        -OrcRoot         $OrcRoot `
        -ProjectRequired $Required

    # --------------------------------------------------
    # Contexto final
    # --------------------------------------------------
    return @{
        RepoRoot     = $RepoRoot
        OrcRoot      = $OrcRoot
        Mode         = $mode
        ProjectModel = $projectModel
        Docker       = if ($projectModel) {
            @{
                NetworkName = "orc-$($projectModel.Project.Name)"
            }
        }
    }
}
