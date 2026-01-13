function Invoke-Psql {
    param (
        [Parameter(Mandatory)]
        [string]$Command,

        [Parameter(Mandatory)]
        [hashtable]$DbConfig,

        [string]$Database = "postgres"
    )

    $env:PGPASSWORD = $DbConfig.Password

    $psqlExe = Resolve-Psql

    $sql = "CREATE DATABASE $($DbConfig.Name);"

    $argString = @(
        "-h", $DbConfig.Host,
        "-p", $DbConfig.Port,
        "-U", $DbConfig.User,
        "-d", "postgres",
        "-v", "ON_ERROR_STOP=1",
        "-c", "`"$sql`""
    ) -join " "

    Write-Host "Ejecutando:"
    Write-Host "$psqlExe $argString"

    $stdoutLog = "$env:TEMP\psql-stdout.log"
    $stderrLog = "$env:TEMP\psql-stderr.log"

    $process = Start-Process `
        -FilePath $psqlExe `
        -ArgumentList $argString `
        -NoNewWindow `
        -Wait `
        -PassThru `
        -RedirectStandardOutput $stdoutLog `
        -RedirectStandardError  $stderrLog

    $stdout = if (Test-Path $stdoutLog) {
        Get-Content $stdoutLog -Raw
    } else { "" }

    $stderr = if (Test-Path $stderrLog) {
        Get-Content $stderrLog -Raw
    } else { "" }

    return @{
        ExitCode = $process.ExitCode
        Stdout   = $stdout
        Stderr   = $stderr
    }
}

function Ensure-PostgresDatabase {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $DbConfig = $Context.ProjectModel.Database

    Write-Host "Verificando base de datos '$($DbConfig.Name)'..."

    $checkSql = "SELECT 1 FROM pg_database WHERE datname = '$($DbConfig.Name)';"

    $result = Invoke-Psql `
        -Command  $checkSql `
        -Db       $DbConfig `
        -Database "postgres"

    if ($result.ExitCode -ne 0) {
        throw "No se pudo verificar la base de datos:`n$($result.Stderr)"
    }

    if ($result.Stdout.Trim() -eq "1") {
        Write-Host "La base '$($DbConfig.Name)' ya existe"
        return
    }

    Write-Host "La base no existe. Creándola..."

    $createSql = "CREATE DATABASE $($DbConfig.Name);"

    $result = Invoke-Psql `
        -Command  $createSql `
        -Db       $DbConfig `
        -Database "postgres"

    if ($result.ExitCode -ne 0) {
        throw "No se pudo crear la base '$($DbConfig.Name)':`n$($result.Stderr)"
    }

    Write-Host "Base de datos '$($DbConfig.Name)' creada correctamente"
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