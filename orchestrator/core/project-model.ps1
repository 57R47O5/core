function Resolve-ProjectModel {
    param (
        [Parameter(Mandatory)]
        [ValidateSet("local", "docker")]
        [string]$Mode,

        [Parameter(Mandatory)]
        [string]$ProjectName,

        [Parameter(Mandatory)]
        [string]$RepoRoot,

        [Parameter(Mandatory)]
        [string]$OrcRoot,

        [Parameter(Mandatory)]
        [bool]$ProjectRequired
    )

. "$OrcRoot\core\backend-runtime.ps1"

    # --- valores comunes ---
    $dbName = $ProjectName
    $dbUser = "postgres"
    $dbPass = "142857"
    $dbPort = 5432

    # --- runtime base (NO romper contrato actual) ---
    $projectModel = @{
        Mode    = $Mode
        Project = @{
            Name = $ProjectName
        }
        Database = @{
            Engine   = "django.db.backends.postgresql"
            Name     = $dbName
            User     = $dbUser
            Password = $dbPass
            Port     = $dbPort
        }
    }

    switch ($Mode) {

        "local" {
            # Django local
            $projectModel.Database.Host = "localhost"

            # Liquibase (infra, dockerizada)
            $projectModel.Liquibase = @{
                Host           = "postgres"
                ChangeLogFile  = "changelog/generated/elecciones/master.yaml"
                WorkDir        = Join-Path $OrcRoot ".orc/runtime/liquibase/$ProjectName"
            }
        }

        "docker" {
            # Django docker
            $projectModel.Database.Host = "postgres"

            # Liquibase (mismo entorno de red)
            $projectModel.Liquibase = @{
                Host           = "postgres"
                ChangeLogFile  = "changelog/generated/elecciones/master.yaml"
                WorkDir        = Join-Path $OrcRoot ".orc/runtime/liquibase/$ProjectName"
            }
        }
    }

    $project = Resolve-OrcProject `
        -RepoRoot $RepoRoot `
        -Args     @($ProjectName) `
        -Required:($ProjectRequired)

    $projectModel.Project = $project

    if ($project.BackendPath) {
        $projectModel.Backend = Resolve-OrcBackendRuntime `
            -Project $project `
            -Mode    $Mode
    }

    return $projectModel
}
