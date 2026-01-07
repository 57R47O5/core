
function Ensure-GlobalNetwork {
    param (
        [Parameter(Mandatory)]
        [string]$NetworkName
    )

    $networks = & docker network ls --format '{{.Name}}'

    if (-not ($networks | Where-Object { $_ -eq $NetworkName })) {
        Write-Host "[orc] creating docker network '$NetworkName'"
        docker network create $NetworkName | Out-Null
    }
}

function Ensure-GlobalPostgres {
    param (
        [Parameter(Mandatory)]
        [string]$NetworkName
    )  

    $PostgresName = "postgres"

    Ensure-GlobalNetwork -NetworkName $NetworkName

    $containerExists = & docker ps -a --format '{{.Names}}' |
        Where-Object { $_ -eq $PostgresName }

    $hasHealthcheck = docker inspect $PostgresName `
    --format '{{if .State.Health}}yes{{else}}no{{end}}' 2>$null

    if ($containerExists -and ($hasHealthcheck -eq "no")) {
    Write-Host "[orc] postgres exists but has no healthcheck - recreating"
    docker rm -f $PostgresName | Out-Null
    $containerExists = $false
    }

    if ($containerExists) {
        Write-Host "[orc] global postgres already exists"
        return
    }

    Write-Host "[orc] starting global postgres"

    $dockerArgs = @(
        "run", "-d",
        "--name", $PostgresName,
        "--network", $NetworkName,
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
    $PostgresName = "postgres"

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
                Write-Error "[orc] postgres has no healthcheck - invalid contract"
                exit 1
            }
            default {
                Start-Sleep -Seconds 2
            }
        }
    }
}
