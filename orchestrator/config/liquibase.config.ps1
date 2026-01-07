function Get-LiquibaseConfig {
    param (
        [Parameter(Mandatory)]
        $ctx
    )

    $db = $ctx.Runtime.Database

    return @{
        Image = "liquibase/liquibase:5.0"

        Workspace = @{
            ContainerPath = "/workspace"
        }

        Volumes = @(
            @{
                HostPath      = { param($ctx) $ctx.LiquibaseRuntimeDocker }
                ContainerPath = "/workspace"
            }
        )

        DefaultsFile = "liquibase.properties"
        Classpath    = "drivers/postgresql-42.7.8.jar"

        Db = @{
            Host     = $db.Host
            Port     = $db.Port
            Name     = $db.Name
            User     = $db.User
            Password = $db.Password
        }
    }
}
