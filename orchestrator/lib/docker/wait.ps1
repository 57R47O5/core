function Wait-GlobalPostgres {
    param ($Config)

    $pgName = $Config.Postgres.Name

    Write-Host "[orc] waiting for global postgres..."

    for ($i = 0; $i -lt 30; $i++) {
        $status = & docker inspect `
            --format '{{.State.Health.Status}}' `
            $pgName 2>$null

        if ($status -eq "healthy") {
            Write-Host "[orc] postgres is healthy"
            return
        }

        Start-Sleep -Seconds 2
    }

    Write-Error "[orc] postgres did not become healthy"
    exit 1
}
