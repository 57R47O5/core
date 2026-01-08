param (
    [Parameter(Mandatory)]
    [string[]]$Args,

    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$LiquibaseRuntime
)

# ------------------------------------------------------------
# Guard rails iniciales
# ------------------------------------------------------------
if ($Args.Count -eq 0) {
    Write-Host "Uso:"
    Write-Host "  orc liquibase version"
    Write-Host "  orc liquibase status"
    Write-Host "  orc liquibase validate"
    Write-Host "  orc liquibase update"
    exit 1
}

if (-not (Test-Path $LiquibaseRuntime)) {
    Write-Error "[orc] Liquibase runtime no existe: $LiquibaseRuntime"
    exit 1
}

# ------------------------------------------------------------
# Infra docker (network, postgres, config)
# ------------------------------------------------------------
$DockerInfra = Join-Path $PSScriptRoot "..\lib\docker-infra.ps1"
. $DockerInfra

# ------------------------------------------------------------
# Helper para volúmenes docker
# ------------------------------------------------------------
function Resolve-DockerVolumes {
    param (
        [array]$Volumes,
        [hashtable]$Context
    )

    $args = @()

    foreach ($v in $Volumes) {
        $host = if ($v.HostPath -is [scriptblock]) {
            & $v.HostPath $Context
        } else {
            $v.HostPath
        }

        $args += "-v"
        $args += "$host:$($v.ContainerPath)"
    }

    return $args
}

# ------------------------------------------------------------
# Acción
# ------------------------------------------------------------
$action = $Args[0]
$rest   = if ($Args.Count -gt 1) { $Args[1..($Args.Count - 1)] } else { @() }

Write-Host "[liquibase] action: $action"
if ($rest.Count -gt 0) {
    Write-Host "[liquibase] extra args: $($rest -join ' ')"
}

# ------------------------------------------------------------
# Docker paths (unix style)
# ------------------------------------------------------------
$LiquibaseRuntimeDocker = ($LiquibaseRuntime -replace '\\', '/')

# ------------------------------------------------------------
# Docker base args
# ------------------------------------------------------------
$liquibaseCfg = $OrcDockerConfig.Liquibase

$dockerBaseArgs = @(
    "run", "--rm",
    "--network", $NetworkName
)

$dockerBaseArgs += Resolve-DockerVolumes `
    -Volumes $liquibaseCfg.Volumes `
    -Context @{ LiquibaseRuntimeDocker = $LiquibaseRuntimeDocker }

$dockerBaseArgs += @(
    "-w", $liquibaseCfg.Workspace.ContainerPath,
    $liquibaseCfg.Image,
    "--defaultsFile=$($liquibaseCfg.DefaultsFile)",
    "--classpath=$($liquibaseCfg.Classpath)"
)

# ------------------------------------------------------------
# Ejecución segura (garantiza Pop-Location)
# ------------------------------------------------------------
Push-Location $LiquibaseRuntime

try {

    switch ($action) {

        "version" {
            Write-Host "[orc] liquibase version"
            & docker @($dockerBaseArgs + @("--version"))
        }

        "validate" {
            Ensure-GlobalNetwork
            Ensure-GlobalPostgres
            Wait-GlobalPostgres

            Write-Host "[orc] liquibase validate"
            & docker @(
                $dockerBaseArgs +
                @(
                    "validate",
                    "--log-level=DEBUG",
                    "--log-file=/workspace/liquibase-debug.log"
                )
            )
        }

        "status" {
            Write-Host "[orc] liquibase status"
            & docker @($dockerBaseArgs + @("status"))
        }

        "update" {
            Ensure-GlobalNetwork
            Ensure-GlobalPostgres
            Wait-GlobalPostgres

            Write-Host "[orc] liquibase update"
            & docker @($dockerBaseArgs + @("update"))
        }

        default {
            Write-Error "Acción liquibase no soportada: $action"
            exit 1
        }
    }

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

}
finally {
    Pop-Location
}

exit 0
