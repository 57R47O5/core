function Resolve-DockerVolumes {
    param (
        [Parameter(Mandatory)]
        [object[]]$Volumes,

        [Parameter(Mandatory)]
        [hashtable]$Context
    )

           
    $args = @()

    foreach ($vol in $Volumes) {
        if (-not $vol.HostPath) {
            throw "Volume.HostPath no definido"
        }

        if (-not $vol.ContainerPath) {
            throw "Volume.ContainerPath no definido"
        }

        # Resolver HostPath (closure o valor directo)
        $hostPath =
            if ($vol.HostPath -is [ScriptBlock]) {
                & $vol.HostPath $Context
            } else {
                $vol.HostPath
            }

        if (-not $hostPath) {
            throw "HostPath resuelto es null"
        }

        $args += @(
            "-v",
            "$hostPath`:$($vol.ContainerPath)"
        )
    }

    return $args
}
