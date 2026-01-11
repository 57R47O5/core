function Invoke-OrcDocker {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context,

        [Parameter(Mandatory)]
        [string[]]$Args
    )

    Write-Host "[orc] docker $($Args -join ' ')"

    # --------------------------------------------------
    # Guardrail: docker run debe tener --name
    # --------------------------------------------------
    if ($Args.Count -gt 0 -and $Args[0] -eq "run") {
        if ($Args -notcontains "--name") {
            Write-Error "[orc] docker run sin --name está prohibido. El nombre del contenedor es obligatorio."
            exit 1
        }
    }

    & docker @Args

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
