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

    switch ($Mode) {

        "local" {
            return @{
                Database = @{
                    Engine   = "django.db.backends.postgresql"
                    Name     = $ProjectName
                    User     = "postgres"
                    Password = "postgres"
                    Host     = "localhost"
                    Port     = 5432
                }
            }
        }

        "docker" {
            return @{
                Database = @{
                    Engine   = "django.db.backends.postgresql"
                    Name     = $ProjectName
                    User     = "postgres"
                    Password = "postgres"
                    Host     = "postgres"
                    Port     = 5432
                }
            }
        }
    }
}
