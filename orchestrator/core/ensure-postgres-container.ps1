function Ensure-PostgresContainer {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $projectModel = $Context.ProjectModel
    $projectName  = $projectModel.Project.Name
    $db           = $projectModel.Database
    $networkName  = $Context.Docker.NetworkName
    $OrcRoot      = $Context.OrcRoot
    $containerName = "$projectName-postgres"

    Write-Host "🐘 Asegurando contenedor Postgres '$containerName'"

    . "$OrcRoot\config\docker.config.ps1"

    # --------------------------------------------------
    # ¿Existe?
    # --------------------------------------------------
    $exists = docker ps -a `
        --filter "name=^${containerName}$" `
        --format "{{.Names}}"

    if (-not $exists) {
        Write-Host "➕ Contenedor Postgres no existe. Creándolo..."

        $pgArgs = @(
            "run", "-d",
            "--name", $containerName,
            "--network", $networkName
        )

        # Env
        $pgArgs += @(
            "-e", "POSTGRES_USER=$($db.User)",
            "-e", "POSTGRES_PASSWORD=$($db.Password)",
            "-e", "POSTGRES_DB=postgres"
        )

        # Imagen
        $pgArgs += "postgres:16"

        Invoke-OrcDocker `
            -Context $Context `
            -Args    $pgArgs
    }
    else {
        # --------------------------------------------------
        # ¿Está corriendo?
        # --------------------------------------------------
        $running = docker ps `
            --filter "name=^${containerName}$" `
            --format "{{.Names}}"

        if ($running) {
            Write-Host "ℹ️  Contenedor Postgres ya está corriendo"
        }
        else {
            Write-Host "▶️  Contenedor Postgres existe pero está detenido. Iniciándolo..."

            Invoke-OrcDocker `
                -Context $Context `
                -Args    @("start", $containerName)
        }
    }

    # --------------------------------------------------
    # Esperar Postgres REALMENTE
    # --------------------------------------------------
    Write-Host "⏳ Esperando que Postgres acepte conexiones..."

    $maxTries = 30
    for ($i = 0; $i -lt $maxTries; $i++) {

        docker exec $containerName `
            pg_isready `
            -U $db.User *> $null

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Postgres listo"
            return
        }

        Start-Sleep -Seconds 2
    }

    throw "❌ Postgres no respondió luego de $maxTries intentos"
}
