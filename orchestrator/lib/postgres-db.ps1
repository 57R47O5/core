function Remove-PostgresDatabase {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $projectModel = $Context.ProjectModel
    $db           = $projectModel.Database

    if (-not $db) {
        throw "El proyecto no define configuración de base de datos"
    }

    $psql = Resolve-Psql

    $env:PGPASSWORD = $db.Password

    $commonArgs = @(
        "-h", $db.Host
        "-p", ($db.Port)
        "-U", $db.User
        "-d", "postgres"
        "-v", "ON_ERROR_STOP=1"
        "-t"
        "-c"
    )

    # 1. ¿Existe la base?
    $checkSql = "SELECT 1 FROM pg_database WHERE datname = '$($db.Name)';"

    $check = & $psql @commonArgs $checkSql 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Error verificando la base de datos:`n$check"
    }

    if ($check.Trim() -ne "1") {
        return
    }

    # 2. Cerrar conexiones activas
    $terminateSql = @"
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '$($db.Name)'
  AND pid <> pg_backend_pid();
"@

    & $psql @commonArgs $terminateSql | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudieron cerrar conexiones activas"
    }

    # 3. Eliminar base
    $dropSql = "DROP DATABASE $($db.Name);"

    
    $drop = & $psql @commonArgs $dropSql 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo eliminar la base '$($db.Name)':`n$drop"
    }
    Write-Host "Base de datos eliminada"
}

function Resolve-Psql {
    $candidates = @(
        "C:\Program Files\PostgreSQL\*\bin\psql.exe",
        "C:\Program Files (x86)\PostgreSQL\*\bin\psql.exe"
    )

    foreach ($pattern in $candidates) {
        $match = Get-ChildItem $pattern -ErrorAction SilentlyContinue |
                 Sort-Object FullName -Descending |
                 Select-Object -First 1

        if ($match) {
            return $match.FullName
        }
    }

    throw "psql.exe no encontrado. Instalá PostgreSQL o agregá psql al PATH."
}