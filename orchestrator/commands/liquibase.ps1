param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$runtime  = $Context.Runtime
$orcRoot  = $Context.OrcRoot
$repoRoot = $Context.RepoRoot
$project  = $runtime.Project

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

# --------------------------------------------------
# Proyecto y modo
# --------------------------------------------------
$project = Resolve-OrcProject `
    -RepoRoot $RepoRoot `
    -Args     $Args `
    -Required

$mode = Resolve-OrcMode -Args $Args

# --------------------------------------------------
# Runtime (FUENTE ÚNICA DE VERDAD)
# --------------------------------------------------
. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\runtime.ps1"

$runtime = Resolve-OrcRuntime `
    -Mode        $mode `
    -ProjectName $project.Name `
    -RepoRoot    $RepoRoot `
    -OrcRoot     $OrcRoot

Write-Host "[orc] liquibase"
Write-Host "  Project: $($runtime.Project.Name)"
Write-Host "  Mode:    $($runtime.Mode)"
Write-Host "  Action:  $action"
Write-Host ""

# --------------------------------------------------
# Docker config (derivada del runtime)
# --------------------------------------------------
. "$OrcRoot\config\docker.config.ps1"

$OrcDockerConfig = Get-OrcDockerConfig -ctx @{
    Runtime = $runtime
}

if (-not $OrcDockerConfig) {
    throw "[orc] OrcDockerConfig no pudo construirse"
}

# --------------------------------------------------
# Liquibase modules
# --------------------------------------------------
$liqRoot = Join-Path $OrcRoot "lib\liquibase"

. "$liqRoot\liquibase.config.ps1"
. "$liqRoot\liquibase.docker.ps1"
. "$liqRoot\liquibase.actions.ps1"
. "$liqRoot\liquibase.validate.ps1"

# --------------------------------------------------
# Liquibase config (UNIFICADA)
# --------------------------------------------------
$cfg = Get-LiquibaseConfig -ctx @{
    Runtime         = $runtime
    OrcDockerConfig = $OrcDockerConfig
}

Assert-LiquibaseConfig $cfg

# --------------------------------------------------
# Docker args
# --------------------------------------------------
$dockerArgs = New-LiquibaseDockerArgs `
    -LiquibaseConfig $cfg `
    -NetworkName     $OrcDockerConfig.GlobalNetwork

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
