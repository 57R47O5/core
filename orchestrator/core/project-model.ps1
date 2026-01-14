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

. "$OrcRoot\core\database-model.ps1"

    # --- valores comunes ---
    $dbName = $ProjectName
    $dbUser = "postgres"
    $dbPass = "142857"
    $dbPort = 5432
    

    $databaseModel = New-DatabaseModel -Config @{
        Name        = $dbName
        Engine      = "django.db.backends.postgresql"
        Host        = "localhost"
        Port        = $dbPort
        User        = $dbUser
        Password    = $dbPass
        NetworkName = ""
    }
    
    # --- runtime base (NO romper contrato actual) ---
    $projectModel = @{
        Mode    = $Mode
        Project = @{
            Name = $ProjectName
        }
        Database = $databaseModel
        Liquibase = @{
        }
    }
    
    $projectModel.Liquibase = @{
        Host          = $databaseModel.Host
        SearchPath    = "C:\Users\Seraf\proyectos\liquibase"
        ChangeLogFile = "changelog/generated/elecciones/master.yaml"
    }
  
    $project = Resolve-OrcProject `
        -RepoRoot $RepoRoot `
        -Args     @($ProjectName) `
        -Required:($ProjectRequired)

    $projectModel.Project = $project

    $projectModel.Backend = @{
        Type = "django"
        Path = $backendPath
        Port = 8000
    }
  
       
    return $projectModel
}
