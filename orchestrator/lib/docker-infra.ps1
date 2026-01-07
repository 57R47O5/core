
. "$PSScriptRoot/../config/docker.config.ps1"

$pg = $OrcDockerConfig.Postgres

function Ensure-GlobalNetwork {

    $networkName = $OrcDockerConfig.GlobalNetwork

    $networks = & docker network ls --format '{{.Name}}'

    if (-not ($networks | Where-Object { $_ -eq $networkName })) {
        Write-Host "[orc] creating docker network '$networkName'"
        docker network create $networkName | Out-Null
    }
}

function Ensure-GlobalPostgres {

    $networkName  = $OrcDockerConfig.GlobalNetwork
    $postgresName = $OrcDockerConfig.GlobalPostgres.Name

    Ensure-GlobalNetwork

    $containerExists = & docker ps -a --format '{{.Names}}' |
        Where-Object { $_ -eq $postgresName }

    $hasHealthcheck = & docker inspect $postgresName `
        --format '{{if .State.Health}}yes{{else}}no{{end}}' 2>$null

    if ($containerExists -and $hasHealthcheck -eq "no") {
        Write-Host "[orc] postgres exists but has no healthcheck — recreating"
        docker rm -f $postgresName | Out-Null
        $containerExists = $false
    }

    if ($containerExists) {
        Write-Host "[orc] global postgres already exists"
        return
    }

    Write-Host "[orc] starting global postgres"

    $dockerArgs = @(
        "run", "-d",
        "--name",    $postgresName,
        "--network", $networkName,
        "-e", "POSTGRES_USER=$($OrcDockerConfig.GlobalPostgres.User)",
        "-e", "POSTGRES_PASSWORD=$($OrcDockerConfig.GlobalPostgres.Password)",
        "-e", "POSTGRES_DB=$($OrcDockerConfig.GlobalPostgres.Database)",
        "-v", "$($OrcDockerConfig.GlobalPostgres.Volume):/var/lib/postgresql/data",
        "--health-cmd",      $hc.Cmd,
        "--health-interval", $hc.Interval,
        "--health-timeout",  $hc.Timeout,
        "--health-retries",  "$($hc.Retries)",
        $OrcDockerConfig.GlobalPostgres.Image
    )
    Write-Host "[orc] docker $($dockerArgs -join ' ')"
    & docker @dockerArgs

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}


function Wait-GlobalPostgres {
    Write-Host "[orc] waiting for global postgres..."

    while ($true) {
        $state = docker inspect $postgresName `
            --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' `
            2>$null

        switch ($state) {
            "healthy" {
                Write-Host "[orc] global postgres is healthy"
                return
            }
            "no-healthcheck" {
                Write-Error "[orc] postgres has no healthcheck - invalid contract"
                exit 1
            }
            default {
                Start-Sleep -Seconds 2
            }
        }
    }
}
