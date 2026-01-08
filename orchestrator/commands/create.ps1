param (
    # Contexto del orco
    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$OrcRoot,

    # Argumentos posicionales del comando
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if ($Args.Count -lt 1) {
    Write-Host "Falta el nombre del proyecto"
    Write-Host "   Uso: orc create <nombre-proyecto>"
    exit 1
}

$project = $Args[0]

$backendPath  = Join-Path $repoRoot "backend\projects\$project"
$frontendPath = Join-Path $repoRoot "frontend\proyectos\$project"

if ((Test-Path $backendPath) -or (Test-Path $frontendPath)) {
    Write-Host "❌ El proyecto '$project' ya existe"
    exit 1
}

$helper = Join-Path $repoRoot "orchestrator\scripts\orc_create_project.py"

if (!(Test-Path $helper)) {
    Write-Host "❌ No se encontró el helper $helper"
    exit 1
}

Write-Host "🐗 Orc creando proyecto '$project' desde orc.yaml"
Write-Host ""

python $helper $project
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host "❌ El helper falló (exit code $exitCode)"
    exit 1
}

# --------------------------------------------------
# Runtime
# --------------------------------------------------
. "$OrcRoot\core\context.ps1"
. "$OrcRoot\core\runtime.ps1"

$runtime = Resolve-OrcRuntime `
    -Mode        "docker" `
    -ProjectName $project `
    -RepoRoot    $RepoRoot `
    -OrcRoot     $OrcRoot

$lbRuntimeDir = $runtime.Liquibase.WorkDir
New-Item -ItemType Directory -Force -Path $lbRuntimeDir | Out-Null

$lbPropsPath = Join-Path $lbRuntimeDir "liquibase.properties"

@"
changeLogFile=${($runtime.Liquibase.ChangeLogFile)}
url=jdbc:postgresql://${($runtime.Liquibase.Host)}:5432/${($runtime.Database.Name)}
username=${($runtime.Database.User)}
password=${($runtime.Database.Password)}
driver=org.postgresql.Driver
defaultSchemaName=public
"@ | Set-Content -Path $lbPropsPath -Encoding UTF8

Write-Host ""
Write-Host "🐗 Inicializando base de datos con Liquibase"

# Delegamos en el orco (fuente única)
& "$OrcRoot\orc.ps1" liquibase update `
    -RepoRoot        $RepoRoot `
    -LiquibaseRuntime $lbRuntimeDir

$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host "❌ Liquibase falló (exit code $exitCode)"
    exit 1
}

Write-Host ""
Write-Host "✅ Proyecto '$project' creado correctamente"
Write-Host "Podés levantarlo con:"
Write-Host "  orc up $project"
