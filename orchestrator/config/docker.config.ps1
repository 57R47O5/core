function Get-OrcDockerConfig {
    param (
        [Parameter(Mandatory)]
        $ctx
    )

    $db           = $ctx.ProjectModel.Database
    $projectModel = $ctx.ProjectModel
    $changeLog    = $projectModel.Liquibase.ChangeLogFile

    if (-not $changeLog) {
        throw "[orc] Liquibase.ChangeLogFile no definido en ProjectModel"
    }

    return @{
        GlobalNetwork = "orc_global"

        Postgres = @{
            Name   = "postgres"
            Image  = "postgres:16"
            Volume = "monorepo-pgdata"
            Port   = $db.Port

            Env = @{
                POSTGRES_USER     = $db.User
                POSTGRES_PASSWORD = $db.Password
                POSTGRES_DB       = $db.Name
            }

            Healthcheck = @{
                Cmd      = "pg_isready -U $($db.User)"
                Interval = "5s"
                Timeout  = "5s"
                Retries  = 5
            }
        }

        Liquibase = @{
            Image = "liquibase/liquibase:5.0"

            # 👈 RELATIVO A /workspace
            ChangeLogFile = $changeLog

            Workspace = @{
                ContainerPath = "/workspace"
            }

            DefaultsFile = "/workspace/liquibase.properties"
            Classpath    = "/liquibase/lib"

            Volumes = @(
                @{
                    HostPath      = Join-Path $RepoRoot "docker/liquibase"
                    ContainerPath = "/workspace"
                }
                @{
                    HostPath      = Join-Path $RepoRoot "docker/liquibase/drivers"
                    ContainerPath = "/liquibase/lib"
                }
            )
        }
    }
}
