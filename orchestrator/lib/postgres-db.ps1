#############################################
# Resolve psql
#############################################

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

#############################################
# Invoke-Psql (núcleo común)
#############################################

function Invoke-Psql {
    param (
        [Parameter(Mandatory)]
        [string]$Command,

        [Parameter(Mandatory)]
        [hashtable]$DbConfig,

        [string]$Database = "postgres"
    )

    $oldPassword = $env:PGPASSWORD
    $env:PGPASSWORD = $DbConfig.Password

    $stdoutLog = "$env:TEMP\psql-stdout.log"
    $stderrLog = "$env:TEMP\psql-stderr.log"

    try {
        $psqlExe = Resolve-Psql

        $argString = @(
            "-h `"$($DbConfig.Host)`""
            "-p $($DbConfig.Port)"
            "-U `"$($DbConfig.User)`""
            "-d `"$Database`""
            "-v ON_ERROR_STOP=1"
            "--echo-errors"
            "-c `"$Command`""
        ) -join " "

        Write-Host "Ejecutando:"
        Write-Host "$psqlExe $argString"

        if (Test-Path $stdoutLog) { Remove-Item $stdoutLog -Force }
        if (Test-Path $stderrLog) { Remove-Item $stderrLog -Force }

        $process = Start-Process `
            -FilePath $psqlExe `
            -ArgumentList $argString `
            -NoNewWindow `
            -Wait `
            -PassThru `
            -RedirectStandardOutput $stdoutLog `
            -RedirectStandardError  $stderrLog

        if (Test-Path $stdoutLog) {
            $stdout = Get-Content $stdoutLog -Raw
        }
        else {
            $stdout = ""
        }

        if (Test-Path $stderrLog) {
            $stderr = Get-Content $stderrLog -Raw
        }
        else {
            $stderr = ""
        }
        
        return @{
            ExitCode = $process.ExitCode
            Stdout   = $stdout
            Stderr   = $stderr
        }
    }
    finally {
        $env:PGPASSWORD = $oldPassword
    }
}


#############################################
# Ensure database exists
#############################################

function Ensure-PostgresDatabase {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $DbConfig = $Context.ProjectModel.Database
    $dbName   = $DbConfig.Name

    Write-Host "Verificando base de datos '$dbName'..."

    $checkSql = @"
SELECT 1
FROM pg_database
WHERE datname = '$dbName';
"@

    $result = Invoke-Psql `
        -Command  $checkSql `
        -DbConfig $DbConfig `
        -Database "postgres"

    if ($result.ExitCode -ne 0) {
        throw "No se pudo verificar la base de datos:`n$($result.Stderr)"
    }

    if ($result.Stdout.Trim() -eq "1") {
        Write-Host "La base '$dbName' ya existe"
        return
    }

    Write-Host "La base no existe. Creándola..."

    $createSql = "CREATE DATABASE `"$dbName`";"

    $result = Invoke-Psql `
        -Command  $createSql `
        -DbConfig $DbConfig `
        -Database "postgres"

    if ($result.ExitCode -ne 0) {
        throw "No se pudo crear la base '$dbName':`n$($result.Stderr)"
    }

    Write-Host "Base de datos '$dbName' creada correctamente"
}

#############################################
# (opcional) Ensure database does NOT exist
#############################################
function Remove-PostgresDatabase {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $DbConfig = $Context.ProjectModel.Database
    $dbName   = $DbConfig.Name

    Write-Host "Eliminando base de datos '$dbName'..."

    #
    # 1. Cerrar conexiones activas
    #
    $terminateSql = @"
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '$dbName'
  AND pid <> pg_backend_pid();
"@

    $result = Invoke-Psql `
        -Command  $terminateSql `
        -DbConfig $DbConfig `
        -Database "postgres"

    if ($result.ExitCode -ne 0) {
        $message = @"
No se pudieron cerrar las conexiones activas a la base '$dbName'.

Detalle:
$result.Stderr
"@
        throw $message
    }

    #
    # 2. Eliminar la base
    #
    $dropSql = "DROP DATABASE IF EXISTS `"$dbName`";"

$result = Invoke-Psql `
    -Command  $dropSql `
    -DbConfig $DbConfig `
    -Database "postgres"

Write-Host "----- RESULTADO DROP DATABASE -----"
Write-Host "ExitCode:"
Write-Host $result.ExitCode
Write-Host "STDOUT:"
Write-Host $result.Stdout
Write-Host "STDERR:"
Write-Host $result.Stderr
Write-Host "----------------------------------"

if ($result.ExitCode -ne 0) {
    throw "PostgreSQL rechazó DROP DATABASE"
}
}