function Resolve-OrcProject {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Project
    )

    $scriptRoot = $PSScriptRoot
    $orcRoot   = Split-Path $scriptRoot -Parent 
    $repoRoot   = Split-Path $orcRoot -Parent 

    $backendPath  = Join-Path $repoRoot "backend\projects\$Project"
    $frontendPath = Join-Path $repoRoot "frontend\proyectos\$Project"

    $result = @{
        Name         = $Project
        RepoRoot     = $repoRoot
        BackendPath  = $null
        FrontendPath = $null
        Type         = @()
    }

    if (Test-Path $backendPath) {
        $result.BackendPath = $backendPath
        $result.Type += "backend"
    }

    if (Test-Path $frontendPath) {
        $result.FrontendPath = $frontendPath
        $result.Type += "frontend"
    }

    if ($result.Type.Count -eq 0) {
        throw "Proyecto '$Project' no encontrado ni en backend ni en frontend"
    }

    return $result
}
