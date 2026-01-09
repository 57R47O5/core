function Invoke-LiquibaseVersion {
    param (
        [Parameter(Mandatory)]
        $DockerArgs,

        [Parameter(Mandatory)]
        $LiquibaseConfig
    )

    Write-Host "deberiamos escribir algo"

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
        "--classpath=$($LiquibaseConfig.Classpath)",
        "--version"
    )

    Write-Host "[orc] liquibase version"
    Write-Host "[DEBUG] docker $($DockerArgs + $cmd -join ' ')"

    & docker @($DockerArgs + $cmd)
}
