function Ensure-PostgresDatabase {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $ProjectModel = $Context.ProjectModel
    $db = $ProjectModel.Database
    $NetworkName = $Context.Docker.NetworkName

    Write-Host "🐘 Verificando base de datos '$($db.Name)'..."
    $pgHost = if ($db.Host -eq "localhost") { "postgres" } else { $db.Host }

    $checkCmd = @(
        "run", "--rm",
        "--network", $NetworkName,
        "-e", "PGPASSWORD=$($db.Password)",
        "postgres:16",
        "psql",
        "-h", $pgHost,
        "-U", $db.User,
        "-d", "postgres",
        "-t",
        "-c",
        "SELECT 1 FROM pg_database WHERE datname='$($db.Name)'"
    )

    $exists = (docker @checkCmd 2>$null).Trim()

    Write-Host "checkCmd es $($checkCmd -join ' ')"
    Write-Host "exists es '$exists'"

    if ($exists -match "1") {
        Write-Host "✅ La base '$($db.Name)' ya existe"
        return
    }

    Write-Host "⚠️  La base no existe. Creándola..."

    $createCmd = @(
        "run", "--rm",
        "--network", $NetworkName,
        "-e", "PGPASSWORD=$($db.Password)",
        "postgres:16",
        "psql",
        "-h", $pgHost,
        "-U", $db.User,
        "-c",
        "CREATE DATABASE $($db.Name);"
    )

    & docker @createCmd

    if ($LASTEXITCODE -ne 0) {
        throw "❌ No se pudo crear la base de datos '$($db.Name)'"
    }

    Write-Host "✅ Base de datos '$($db.Name)' creada correctamente"
}

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
        "-p", ($db.Port ?? 5432)
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
}

