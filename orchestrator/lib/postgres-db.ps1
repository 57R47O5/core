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

function Ensure-PostgresDatabase {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $ProjectModel = $Context.ProjectModel
    $db = $ProjectModel.Database
    $NetworkName = $Context.Docker.NetworkName

    Write-Host "Verificando existencia de la base '$($db.Name)'..."

    $checkCmd = @(
        "run", "--rm",
        "--network", $NetworkName,
        "-e", "PGPASSWORD=$($db.Password)",
        "postgres:16",
        "psql",
        "-h", $db.Host,
        "-U", $db.User,
        "-d", "postgres",
        "-t",
        "-c",
        "SELECT 1 FROM pg_database WHERE datname='$($db.Name)'"
    )

    $exists = (docker @checkCmd 2>$null).Trim()

    if ($exists -notmatch "1") {
        Write-Host "La base '$($db.Name)' no existe. Nada que destruir."
        return
    }

    Write-Host "Eliminando base de datos '$($db.Name)'..."

    $dropCmd = @(
        "run", "--rm",
        "--network", $NetworkName,
        "-e", "PGPASSWORD=$($db.Password)",
        "postgres:16",
        "psql",
        "-h", $db.Host,
        "-U", $db.User,
        "-d", "postgres",
        "-c",
        "DROP DATABASE $($db.Name);"
    )

    & docker @dropCmd

    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo eliminar la base de datos '$($db.Name)'"
    }

    Write-Host "Base de datos '$($db.Name)' eliminada correctamente"
}
