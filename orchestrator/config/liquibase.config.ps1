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

        Volumes = $lb.Volumes

        Classpath    = $lb.Classpath
        DefaultsFile = $lb.DefaultsFile

        Runtime = @{
            ProjectRoot = $project.Paths.RepoRoot
            Liquibase   = $project.Liquibase
        }

        Db = @{
            Host     = $db.Host
            Port     = $db.Port
            Name     = $db.Name
            User     = $db.User
            Password = $db.Password
        }
    }
}
