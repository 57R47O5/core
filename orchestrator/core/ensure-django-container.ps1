function Ensure-DjangoContainer {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $projectModel  = $Context.ProjectModel
    $docker        = $Context.Docker
    $django        = $docker.Config.Django
    $OrcRoot       = $Context.OrcRoot
    $networkName   = $docker.NetworkName
    $containerName = $django.Name

    . "$OrcRoot\config\docker.config.ps1"
    Write-Host "🎭 Asegurando contenedor Django '$containerName'"

    # --------------------------------------------------
    # ¿Existe?
    # --------------------------------------------------
    $exists = docker ps -a `
        --filter "name=^${containerName}$" `
        --format "{{.Names}}"

    if (-not $exists) {
        Write-Host "➕ Contenedor Django no existe. Creándolo..."

        $args = @(
            "run", "-d",
            "--name", $containerName,
            "--network", $networkName
        )

        # Ports
        foreach ($p in $django.Ports) {
            $args += @("-p", $p)
        }

        # Env
        foreach ($k in $django.Env.Keys) {
            $args += @("-e", "$k=$($django.Env[$k])")
        }

        # Volumes
        foreach ($v in $django.Volumes) {
            $args += @("-v", "$($v.HostPath):$($v.ContainerPath)")
        }

        # Image
        $args += $django.Image

        # Command
        if ($django.Command) {
            if ($django.Command -is [array]) {
                $args += $django.Command
            }
            else {
                $args += ($django.Command -split " ")
            }
        }

        Invoke-OrcDocker `
            -Context $Context `
            -Args    $args

        Write-Host "✅ Contenedor Django creado y corriendo"
        return
    }

    # --------------------------------------------------
    # ¿Está corriendo?
    # --------------------------------------------------
    $running = docker ps `
        --filter "name=^${containerName}$" `
        --format "{{.Names}}"

    if ($running) {
        Write-Host "ℹ️  Contenedor Django ya está corriendo"
        return
    }

    Write-Host "▶️  Contenedor Django existe pero está detenido. Iniciándolo..."

    Invoke-OrcDocker `
        -Context $Context `
        -Args    @("start", $containerName)

    Write-Host "✅ Contenedor Django iniciado correctamente"
}
