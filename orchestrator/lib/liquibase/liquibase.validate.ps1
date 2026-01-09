function Assert-LiquibaseConfig {
    param (
        [Parameter(Mandatory)]
        [hashtable]$LiquibaseConfig
    )

    # --------------------------------------------------
    # Imagen
    # --------------------------------------------------
    if (-not $LiquibaseConfig.Image) {
        throw "Liquibase.Image no definido"
    }

    # --------------------------------------------------
    # Workspace
    # --------------------------------------------------
    if (-not $LiquibaseConfig.Workspace) {
        throw "Liquibase.Workspace no definido"
    }

    if (-not $LiquibaseConfig.Workspace.ContainerPath) {
        throw "Liquibase.Workspace.ContainerPath no definido"
    }

    # --------------------------------------------------
    # Volúmenes
    # --------------------------------------------------
    if (-not $LiquibaseConfig.Volumes -or $LiquibaseConfig.Volumes.Count -eq 0) {
        throw "Liquibase.Volumes no definido o vacío"
    }

    foreach ($v in $LiquibaseConfig.Volumes) {
        if (-not $v.ContainerPath) {
            throw "Liquibase.Volume.ContainerPath no definido"
        }
    }

    # --------------------------------------------------
    # DB
    # --------------------------------------------------
    $db = $LiquibaseConfig.Db
    if (-not $db) {
        throw "Liquibase.Db no definido"
    }

    foreach ($field in @("Host", "Port", "Name", "User", "Password")) {
        if (-not $db.$field) {
            throw "Liquibase.Db.$field no definido"
        }
    }

    # --------------------------------------------------
    # Defaults / classpath
    # --------------------------------------------------
    if (-not $LiquibaseConfig.DefaultsFile) {
        throw "Liquibase.DefaultsFile no definido"
    }

    if (-not $LiquibaseConfig.Classpath) {
        throw "Liquibase.Classpath no definido"
    }
  
}
