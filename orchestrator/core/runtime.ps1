function Resolve-OrcRuntime {
    param (
        [Parameter(Mandatory)]
        [ValidateSet("local", "docker")]
        [string]$Mode,

        [Parameter(Mandatory)]
        [string]$ProjectName,

        [Parameter(Mandatory)]
        [string]$RepoRoot,

        [Parameter(Mandatory)]
        [string]$OrcRoot
    )

    # --- valores comunes ---
    $dbName = $ProjectName
    $dbUser = "postgres"
    $dbPass = "postgres"
    $dbPort = 5432

    # --- runtime base (NO romper contrato actual) ---
    $runtime = @{
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
            $runtime.Database.Host = "localhost"

            # Liquibase (infra, dockerizada)
            $runtime.Liquibase = @{
                Host           = "postgres"
                ChangeLogFile  = "changelog/generated/elecciones/master.yaml"
                WorkDir        = Join-Path $OrcRoot ".orc/runtime/liquibase/$ProjectName"
            }
        }

        "docker" {
            # Django docker
            $runtime.Database.Host = "postgres"

            # Liquibase (mismo entorno de red)
            $runtime.Liquibase = @{
                Host           = "postgres"
                ChangeLogFile  = "changelog/generated/elecciones/master.yaml"
                WorkDir        = Join-Path $OrcRoot ".orc/runtime/liquibase/$ProjectName"
            }
        }
    }

    return $runtime
}
