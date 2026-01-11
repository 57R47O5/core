param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$orcRoot  = $Context.OrcRoot

# --------------------------------------------------
# Guard rails
# --------------------------------------------------
if ($Args.Count -eq 0) {
    Write-Host "Uso:"
    Write-Host "  orc liquibase <proyecto> <accion> [--local|--docker]"
    Write-Host ""
    Write-Host "Acciones:"
    Write-Host "  version | validate | status | update"
    exit 1
}

$action = $Args | Where-Object { $_ -notmatch '^--' } | Select-Object -Last 1

Write-Host "[orc] liquibase"
Write-Host "  Project: $($projectModel.Project.Name)"
Write-Host "  Mode:    $($projectModel.Mode)"
Write-Host "  Action:  $action"
Write-Host ""

# --------------------------------------------------
# Docker config (derivada del projectModel)
# --------------------------------------------------
. "$OrcRoot\config\docker.config.ps1"
. "$OrcRoot\config\liquibase.config.ps1"

$OrcDockerConfig = Get-OrcDockerConfig -ctx @{
    ProjectModel = $projectModel
}

if (-not $OrcDockerConfig) {
    throw "[orc] OrcDockerConfig no pudo construirse"
}

# --------------------------------------------------
# Liquibase modules
# --------------------------------------------------
$liqRoot = Join-Path $OrcRoot "lib\liquibase"

. "$liqRoot\liquibase.docker.ps1"
. "$liqRoot\liquibase.actions.ps1"
. "$liqRoot\liquibase.validate.ps1"

# --------------------------------------------------
# Liquibase config
# --------------------------------------------------
$cfg = Get-LiquibaseConfig -ctx @{
    ProjectModel    = $projectModel
    OrcDockerConfig = $OrcDockerConfig
}

Assert-LiquibaseConfig $cfg

# --------------------------------------------------
# Docker args
# --------------------------------------------------
$dockerArgs = New-LiquibaseDockerArgs `
    -LiquibaseConfig $cfg `
    -NetworkName     $Context.Docker.NetworkName

# --------------------------------------------------
# Dispatch
# --------------------------------------------------
switch ($action) {

    "version" {
        Invoke-LiquibaseVersion `
            -DockerArgs $dockerArgs `
            -LiquibaseConfig $cfg
    }

    "validate" {
        Invoke-LiquibaseValidate `
            -DockerArgs $dockerArgs `
            -LiquibaseConfig $cfg
    }

    "status" {
        Invoke-LiquibaseStatus `
            -DockerArgs $dockerArgs `
            -LiquibaseConfig $cfg
    }

    "update" {
        Invoke-LiquibaseUpdate `
            -DockerArgs $dockerArgs `
            -LiquibaseConfig $cfg
    }

    default {
        throw "[orc] Acción liquibase no soportada: $action"
    }
}

exit $LASTEXITCODE
