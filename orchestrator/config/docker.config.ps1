function Get-OrcDockerConfig {
    param (
        [Parameter(Mandatory)]
        $ctx
    )

    $projectModel = $ctx.ProjectModel
    $db           = $projectModel.Database
    $changeLog    = $projectModel.Liquibase.ChangeLogFile

    if (-not $changeLog) {
        throw "[orc] Liquibase.ChangeLogFile no definido en ProjectModel"
    }

    return @{
        Postgres = @{
            Name   = $db.Host
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
            Name = "liquibase"
            Image = "liquibase/liquibase:5.0"

            # RELATIVO A /workspace
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

        Django = @{
            Name = "django"
            Image = "$($projectModel.Project.Name)-django"
            BaseImage   = "python:3.12-slim"

            Dockerfile  = "docker\Dockerfile.backend"
            BuildContext = $Context.RepoRoot

            Workdir = "/app"
            Command = "python manage.py runserver 0.0.0.0:8000"

            Env = @{
                DB_ENGINE   = $db.Engine
                DB_NAME     = $db.Name
                DB_USER     = $db.User
                DB_PASSWORD = $db.Password
                DB_HOST     = $db.Host
                DB_PORT     = $db.Port
            }

            Volumes = @(
                @{
                    HostPath      = $projectModel.Project.BackendPath
                    ContainerPath = "/app"
                }
            )

            Ports = @(
                "8000:8000"
            )

            DependsOn = @("postgres")
        }
    }
}
