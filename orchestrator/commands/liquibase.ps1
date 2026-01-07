param (
    [Parameter(Mandatory)]
    [string[]]$Args,

    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$LiquibaseRuntime
)

$DockerInfra = Join-Path $PSScriptRoot "..\lib\docker-infra.ps1"
. $DockerInfra

# ------------------------------------------------------------
# Guard rails
# ------------------------------------------------------------
if ($Args.Count -eq 0) {
    Write-Host "Uso:"
    Write-Host "  orc liquibase version"
    Write-Host "  orc liquibase status"
    Write-Host "  orc liquibase validate"
    Write-Host "  orc liquibase update"
    exit 1
}

# ------------------------------------------------------------
# Helper para expandir volúmenes
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



$action = $Args[0]
$rest   = $Args[1..($Args.Count - 1)]

Write-Host "[liquibase] action: $action"
if ($rest.Count -gt 0) {
    Write-Host "[liquibase] extra args: $($rest -join ' ')"
}

# ------------------------------------------------------------
# Runtime paths (orc owns filesystem)
# ------------------------------------------------------------
$LiquibaseRuntime = Join-Path $OrcRoot "runtime\liquibase"

New-Item -ItemType Directory -Force -Path $LiquibaseRuntime | Out-Null

# ------------------------------------------------------------
# Prepare runtime content
# ------------------------------------------------------------
Copy-Item (Join-Path $RepoRoot "docker\liquibase\liquibase.properties") `
          $LiquibaseRuntime -Force

Copy-Item (Join-Path $RepoRoot "docker\liquibase\changelog") `
          $LiquibaseRuntime -Recurse -Force

Copy-Item (Join-Path $RepoRoot "docker\liquibase\drivers") `
          $LiquibaseRuntime -Recurse -Force

# ------------------------------------------------------------
# Docker paths MUST be Unix style
# ------------------------------------------------------------
$LiquibaseRuntimeDocker = ($LiquibaseRuntime -replace '\\', '/')

# ------------------------------------------------------------
# Base docker args (ARRAY — no backticks)
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
# Dispatch liquibase actions
# ------------------------------------------------------------
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
        & docker @($dockerBaseArgs + @("validate"))
        "--log-level=DEBUG",
        "--log-file=$RepoRoot/liquibase-debug.log"
    }

    "status" {
        Write-Host "[orc] liquibase status"
        & docker @($dockerBaseArgs + @("status"))

    }

    "update" {
        # Infra dependency — responsabilidad del orco
        Ensure-GlobalNetwork
        Ensure-GlobalPostgres
        Wait-GlobalPostgres

        Write-Host "[orc] liquibase update"
        & docker @($dockerBaseArgs + @("update"))
    }

    default {
        Write-Host "Acción liquibase no soportada: $action"
        exit 1
    }
}

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

exit 0