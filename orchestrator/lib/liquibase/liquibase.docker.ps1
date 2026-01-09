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

    $args += Resolve-DockerVolumes `
        -Volumes $LiquibaseConfig.Volumes `
        -Context @{ LiquibaseRuntimeDocker = $LiquibaseConfig.RuntimeDocker }

    $args += @(
        "-w", $LiquibaseConfig.Workspace.ContainerPath,
        $LiquibaseConfig.Image
    )

    return $args
}
