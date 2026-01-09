function Assert-LiquibaseConfig {
    param ($LiquibaseConfig)

    if (-not $LiquibaseConfig.Image) {
        throw "Liquibase.Image no definido"
    }

    if (-not (Test-Path $LiquibaseConfig.RuntimeHost)) {
        throw "Liquibase runtime no existe: $($LiquibaseConfig.RuntimeHost)"
    }
}
