function Ensure-LiquibaseWorkspace {
    param (
        [Parameter(Mandatory)]
        [string]$Root
    )

    $lbRoot = Join-Path $Root ".orco\liquibase"

    if (-not (Test-Path $lbRoot)) {
        New-Item -ItemType Directory -Path $lbRoot | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $lbRoot "changelog") | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $lbRoot "runtime") | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $lbRoot "logs") | Out-Null
    }

    return @{
        Root    = $lbRoot
        Runtime = Join-Path $lbRoot "runtime"
    }
}
