function Invoke-LiquibaseVersion {
    param (
        [Parameter(Mandatory)]
        $DockerArgs,

        [Parameter(Mandatory)]
        $LiquibaseConfig
    )

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
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

    $db = $LiquibaseConfig.Db

    $jdbcUrl = "jdbc:postgresql://$($db.Host):$($db.Port)/$($db.Name)"

    $cmd = @(
        "--url=$jdbcUrl",
        "--username=$($db.User)",
        "--password=$($db.Password)",
        "--changeLogFile=$($LiquibaseConfig.ChangeLogFile)",
        "update"
    )

    Write-Host "[orc] liquibase update"
    Write-Host "[DEBUG] docker $($DockerArgs + $cmd -join ' ')"

    & docker @($DockerArgs + $cmd)
}

