function Resolve-OrcBackendRuntime {
    param (
        [Parameter(Mandatory)]
        $Project,

        [Parameter(Mandatory)]
        [string]$Mode
    )

    $root = $Project.BackendPath

    $venvPath = Join-Path $root ".venv"

    return @{
        Root       = $root
        VenvPath   = $venvPath
        ActivatePs = Join-Path $venvPath "Scripts\activate.ps1"
        PythonExe  = Join-Path $venvPath "Scripts\python.exe"
        ManagePy   = Join-Path $root "manage.py"
        Exists     = Test-Path $venvPath
        Mode       = $Mode
    }
}