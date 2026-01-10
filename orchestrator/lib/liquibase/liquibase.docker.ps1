function New-LiquibaseDockerArgs {
    param (
        [Parameter(Mandatory)]
        $LiquibaseConfig,

        [Parameter(Mandatory)]
        $NetworkName
    )

    $args = @(
        "run", "--rm",
        "--network", $NetworkName
    )

    $dockerLib = Join-Path $OrcRoot "lib\docker"
    . "$dockerLib\docker.volumes.ps1"

    $args += Resolve-DockerVolumes `
        -Volumes $LiquibaseConfig.Volumes `
        -Context @{ LiquibaseRuntimeDocker = $LiquibaseConfig.RuntimeDocker }

    $args += @(
        "-w", $LiquibaseConfig.Workspace.ContainerPath,
        $LiquibaseConfig.Image
    )

    return $args
}
