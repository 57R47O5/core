function Invoke-LiquibaseVersion {
    param (
        [Parameter(Mandatory)]
        $DockerArgs,

        [Parameter(Mandatory)]
        $LiquibaseConfig
    )

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
        "--classpath=$($LiquibaseConfig.Classpath)",
        "version"
    )

    Write-Host "[orc] liquibase version"
    Write-Host "[DEBUG] docker $($DockerArgs + $cmd -join ' ')"

    & docker @($DockerArgs + $cmd)
}

function Invoke-LiquibaseVersion {
    param (
        [Parameter(Mandatory)]
        $DockerArgs,

        [Parameter(Mandatory)]
        $LiquibaseConfig
    )

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
        "--classpath=$($LiquibaseConfig.Classpath)",
        "version"
    )

    Write-Host "[orc] liquibase version"
    Write-Host "[DEBUG] docker $($DockerArgs + $cmd -join ' ')"

    & docker @($DockerArgs + $cmd)
}

function Invoke-LiquibaseValidate {
    param (
        [Parameter(Mandatory)]
        $DockerArgs,

        [Parameter(Mandatory)]
        $LiquibaseConfig
    )

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
        "--classpath=$($LiquibaseConfig.Classpath)",
        "--changeLogFile=$($LiquibaseConfig.ChangeLogFile)",
        "validate"
    )

    Write-Host "[orc] liquibase validate"
    Write-Host "[DEBUG] docker $($DockerArgs + $cmd -join ' ')"

    & docker @($DockerArgs + $cmd)
}

function Invoke-LiquibaseUpdate {
    param (
        [Parameter(Mandatory)]
        $DockerArgs,

        [Parameter(Mandatory)]
        $LiquibaseConfig
    )

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
        "--classpath=$($LiquibaseConfig.Classpath)",
        "--changeLogFile=$($LiquibaseConfig.ChangeLogFile)",
        "update"
    )

    Write-Host "[orc] liquibase update"
    Write-Host "[DEBUG] docker $($DockerArgs + $cmd -join ' ')"

    & docker @($DockerArgs + $cmd)
}


