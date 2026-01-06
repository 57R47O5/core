param (
    [Parameter(Mandatory)]
    [string[]]$Args,

    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$LiquibaseRuntime
)

# ------------------------------------------------------------
# Prepare runtime (orc owns the filesystem)
# ------------------------------------------------------------
New-Item -ItemType Directory -Force -Path $LiquibaseRuntime | Out-Null

Copy-Item (Join-Path $RepoRoot "docker\liquibase\liquibase.properties") `
          $LiquibaseRuntime -Force

Copy-Item (Join-Path $RepoRoot "docker\liquibase\changelog") `
          $LiquibaseRuntime -Recurse -Force

Copy-Item (Join-Path $RepoRoot "docker\liquibase\drivers") `
          $LiquibaseRuntime -Recurse -Force

Write-Host "[orc] liquibase $($Args -join ' ')"

# ------------------------------------------------------------
# Docker paths MUST be Unix style
# ------------------------------------------------------------
$LiquibaseRuntimeDocker = ($LiquibaseRuntime -replace '\\', '/')

# ------------------------------------------------------------
# Docker args (ARRAY — no backticks)
# ------------------------------------------------------------
$dockerArgs = @(
    "run", "--rm",
    "-v", "${LiquibaseRuntimeDocker}:/workspace",
    "-w", "/workspace",
    "liquibase/liquibase:5.0",
    "--defaultsFile=liquibase.properties",
    "--classpath=drivers/postgresql-42.7.8.jar"
) + $Args

Write-Host "[orc] docker $($dockerArgs -join ' ')"

& docker @dockerArgs

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
