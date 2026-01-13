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
# Liquibase modules
# --------------------------------------------------
$liqRoot = Join-Path $OrcRoot "lib\liquibase"

. "$liqRoot\liquibase.actions.ps1"
. "$liqRoot\liquibase.validate.ps1"


# --------------------------------------------------
# Dispatch
# --------------------------------------------------
switch ($action) {

    "version" {
        Invoke-LiquibaseVersion `
            -Context $Context
    }

    "validate" {
        Invoke-LiquibaseValidate `
            -Context $Context
    }

    "status" {
        Invoke-LiquibaseStatus `
            -Context $Context
    }

    "update" {
        Invoke-LiquibaseUpdate `
            -Context $Context
    }

    default {
        throw "[orc] Acción liquibase no soportada: $action"
    }
}

exit $LASTEXITCODE
