Liquibase = @{
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

    Classpath = "drivers/postgresql-42.7.8.jar"
}

