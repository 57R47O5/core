$OrcDockerConfig = @{
    GlobalNetwork = "orc_global"

    Postgres = @{
        Name    = "postgres"
        Image   = "postgres:16"
        Volume  = "monorepo-pgdata"
        Port    = 5433

        Env = @{
            POSTGRES_USER     = "postgres"
            POSTGRES_PASSWORD = "142857"
            POSTGRES_DB       = "postgres"
        }

        Healthcheck = @{
            Cmd      = "pg_isready -U postgres"
            Interval = "5s"
            Timeout  = "5s"
            Retries  = 5
        }
    }
}
