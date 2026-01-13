function Invoke-LiquibaseUpdate {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $db = $Context.ProjectModel.Database

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
        "version"
    )

    Write-Host "[orc] liquibase version"
    Write-Host "[DEBUG] docker $($DockerArgs + $cmd -join ' ')"

    & docker @($DockerArgs + $cmd)
}

function Invoke-LiquibaseUpdate {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $db = $Context.ProjectModel.Database

    $cmd = @(
        "--defaultsFile=$($LiquibaseConfig.Defaults)",
        "--changeLogFile=$($LiquibaseConfig.ChangeLogFile)",
        "validate"
    )

    Write-Host "[orc] liquibase validate"
}

function Invoke-LiquibaseUpdate {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $db = $Context.ProjectModel.Database

    $jdbcUrl = "jdbc:postgresql://$($db.Host):$($db.Port)/$($db.Name)"

    $cmd = @(
        "--url=$jdbcUrl"
        "--username=$($db.User)"
        "--password=$($db.Password)"
        "--changeLogFile=$($Context.ProjectModel.Liquibase.ChangeLogFile)"
        "update"
    )

    Write-Host "[orc] liquibase update"
    Write-Host "[DEBUG] liquibase $($cmd -join ' ')"

    & liquibase @cmd
}


