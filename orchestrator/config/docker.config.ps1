function Get-OrcDockerConfig {
    param (
        [Parameter(Mandatory)]
        $ctx
    )

    $db = $ctx.ProjectModel.Database

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
            Image = "liquibase/liquibase:4.27"

            Workspace = @{
                ContainerPath = "/workspace"
            }

            DefaultsFile = "/workspace/liquibase.properties"
            Classpath    = "/workspace/drivers"

            Volumes = @(
                @{
                    HostPath = { param($ctx) $ctx.LiquibaseRuntimeDocker }
                    ContainerPath = "/workspace"
                }
            )
        }
    }
}
