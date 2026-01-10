function Get-LiquibaseConfig {
    param (
        [Parameter(Mandatory)]
        [hashtable]$ctx
    )

    if (-not $ctx.ProjectModel) {
        throw "ctx.ProjectModel es obligatorio"
    }

    if (-not $ctx.OrcDockerConfig) {
        throw "ctx.OrcDockerConfig es obligatorio"
    }

    $project = $ctx.ProjectModel
    $docker  = $ctx.OrcDockerConfig
    $db      = $project.Database
    $lb      = $docker.Liquibase
    $plb     = $project.Liquibase

    if (-not $lb) {
        throw "Liquibase no definido en OrcDockerConfig"
    }

    if (-not $plb) {
        throw "ProjectModel.Liquibase no definido"
    }

    if (-not $plb.Host) {
        throw "ProjectModel.Liquibase.Host no definido"
    }

    # Normalizar volumes
    $volumes = $lb.Volumes
    if ($volumes -is [hashtable]) {
        $volumes = @($volumes)
    }

    if (-not ($volumes -is [object[]])) {
        throw "[orc] Liquibase.Volumes debe ser array o hashtable"
    }

    return @{
        Image = $lb.Image

        Workspace = $lb.Workspace
        Volumes   = $volumes

        ChangeLogFile = $plb.ChangeLogFile
        Classpath     = $lb.Classpath
        DefaultsFile  = $lb.DefaultsFile

        # 🔑 Host correcto para Liquibase
        Host = $plb.Host

        Db = @{
            Port     = $db.Port
            Name     = $db.Name
            User     = $db.User
            Password = $db.Password
        }

        Runtime = @{
            Liquibase = $plb
        }
    }
}
