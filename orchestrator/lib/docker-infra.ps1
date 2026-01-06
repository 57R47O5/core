."$PSScriptRoot\lib\docker-infra.ps1"

function Ensure-GlobalNetwork {
    param (
        [Parameter(Mandatory)]
        [string]$NetworkName
    )

    if (-not (docker network ls --format "{{.Name}}" |
        Where-Object { $_ -eq $NetworkName })) {

        Write-Host "[orc] creating docker network '$NetworkName'"
        docker network create $NetworkName | Out-Null
    }
}

function Ensure-GlobalPostgres {
    param (
        [Parameter(Mandatory)]
        [string]$PostgresName,
        [Parameter(Mandatory)]
        [string]$NetworkName
    )

    Ensure-GlobalNetwork -NetworkName $NetworkName

    $containerExists = docker ps -a --format "{{.Names}}" |
        Where-Object { $_ -eq $PostgresName }

    if ($containerExists) {
        Write-Host "[orc] global postgres already exists"
        return
    }

    Write-Host "[orc] starting global postgres"

    $dockerArgs = @(
        "run", "-d",
        "--name", $PostgresName,
        "--network", $NetworkName,
        "-p", "5433:5432",
        "-e", "POSTGRES_USER=postgres",
        "-e", "POSTGRES_PASSWORD=142857",
        "-e", "POSTGRES_DB=postgres",
        "-v", "monorepo-pgdata:/var/lib/postgresql/data",
        "--health-cmd", "pg_isready -U postgres",
        "--health-interval", "5s",
        "--health-timeout", "5s",
        "--health-retries", "5",
        "postgres:16"
    )

    Write-Host "[orc] docker $($dockerArgs -join ' ')"
    & docker @dockerArgs

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

function Wait-GlobalPostgres {
    param (
        [Parameter(Mandatory)]
        [string]$PostgresName
    )

    Write-Host "[orc] waiting for global postgres..."

    while ($true) {
        $state = docker inspect $PostgresName `
            --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' `
            2>$null

        switch ($state) {
            "healthy" {
                Write-Host "[orc] global postgres is healthy"
                return
            }
            "no-healthcheck" {
                Write-Error "[orc] postgres has no healthcheck — invalid contract"
                exit 1
            }
            default {
                Start-Sleep -Seconds 2
            }
        }
    }
}
