function Ensure-GlobalPostgres {
    param ($Config)

    $pg = $Config.Postgres
    $hc = $pg.Healthcheck

    Ensure-GlobalNetwork $Config

    $containerExists = & docker ps -a --format '{{.Names}}' |
        Where-Object { $_ -eq $pg.Name }

    $hasHealthcheck = & docker inspect $pg.Name `
        --format '{{if .State.Health}}yes{{else}}no{{end}}' 2>$null

    if ($containerExists -and $hasHealthcheck -eq "no") {
        Write-Host "[orc] postgres exists but has no healthcheck - recreating"
        docker rm -f $pg.Name | Out-Null
        $containerExists = $false
    }

    if ($containerExists) {
        Write-Host "[orc] global postgres already exists"
        return
    }

    Write-Host "[orc] starting global postgres"

    & docker run -d `
        --name $pg.Name `
        --network $Config.GlobalNetwork `
        -e POSTGRES_USER=$($pg.Env.POSTGRES_USER) `
        -e POSTGRES_PASSWORD=$($pg.Env.POSTGRES_PASSWORD) `
        -e POSTGRES_DB=$($pg.Env.POSTGRES_DB) `
        -v "$($pg.Volume):/var/lib/postgresql/data" `
        --health-cmd "$($hc.Cmd)" `
        --health-interval $hc.Interval `
        --health-timeout $hc.Timeout `
        --health-retries $hc.Retries `
        $pg.Image
}
