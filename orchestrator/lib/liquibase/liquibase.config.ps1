function Get-LiquibaseConfig {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Runtime,

        [Parameter(Mandatory)]
        [hashtable]$OrcDockerConfig
    )

    $lb = $OrcDockerConfig.Liquibase
    if (-not $lb) {
        throw "Liquibase no definido en OrcDockerConfig"
    }

    if (-not $lb.Image) {
        throw "Liquibase.Image no definido"
    }

    return @{
        Image      = $lb.Image
        Volumes    = $lb.Volumes
        Workspace  = $lb.Workspace
        Classpath  = $lb.Classpath
        Defaults   = $lb.DefaultsFile
        Runtime    = $Runtime
    }
}
