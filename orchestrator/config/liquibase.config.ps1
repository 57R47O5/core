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

    if (-not $lb) {
        throw "Liquibase no definido en OrcDockerConfig"
    }

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

        ChangeLogFile = $ctx.ProjectModel.Liquibase.ChangeLogFile
        Classpath     = $lb.Classpath
        DefaultsFile  = $lb.DefaultsFile
        Host = $lb.Host

        Db = @{
            Port     = $db.Port
            Name     = $db.Name
            User     = $db.User
            Password = $db.Password
            Host     = $db.Host
        }

        Runtime = @{
            Liquibase = $lb
        }
    }
}
