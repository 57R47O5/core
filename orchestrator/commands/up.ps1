param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel = $Context.ProjectModel
$projectName  = $projectModel.Project.Name
$docker       = $Context.Docker
$OrcRoot      = $Context.OrcRoot

Write-Host "Levantando proyecto '$projectName'"

. "$OrcRoot\config\docker.config.ps1"
. "$OrcRoot\core\docker-container.ps1"
. "$OrcRoot\config\liquibase.config.ps1"
. "$OrcRoot\commands\docker.ps1"
. "$OrcRoot\lib\postgres-db.ps1"

# --------------------------------------------------
# Obtener configuración Docker derivada
# --------------------------------------------------
$dockerConfig = Get-OrcDockerConfig -ctx $Context
$networkName  = $docker.NetworkName

# --------------------------------------------------
# Network
# --------------------------------------------------
Write-Host "Asegurando network '$networkName'"

docker network inspect $networkName *> $null

if ($LASTEXITCODE -ne 0) {
    Invoke-OrcDocker `
        -Context $Context `
        -Args @("network", "create", $networkName) | Out-Null
}

# --------------------------------------------------
# Postgres
# --------------------------------------------------
Write-Host "Levantando Postgres"

Ensure-DockerContainerAbsent `
    -Name $dockerConfig.Postgres.Name

$pgArgs = @(
    "run", "-d",
    "--name", $dockerConfig.Postgres.Name,
    "--network", $networkName,
    "-p", "$($dockerConfig.Postgres.Port):5432",
    "-v", "$($dockerConfig.Postgres.Volume):/var/lib/postgresql/data"
)

foreach ($k in $dockerConfig.Postgres.Env.Keys) {
    $pgArgs += @("-e", "$k=$($dockerConfig.Postgres.Env[$k])")
}

$pgArgs += $dockerConfig.Postgres.Image

Invoke-OrcDocker `
    -Context $Context `
    -Args $pgArgs

# --------------------------------------------------
# Esperar Postgres
# --------------------------------------------------
Write-Host "Esperando Postgres..."

$maxTries = 20
for ($i = 0; $i -lt $maxTries; $i++) {

    Invoke-OrcDocker `
        -Context $Context `
        -Args @( `
            "exec",
            $dockerConfig.Postgres.Name,
            "pg_isready",
            "-U", $projectModel.Database.User
        ) *> $null

    if ($LASTEXITCODE -eq 0) {
        break
    }

    Start-Sleep -Seconds 2
}

if ($i -eq $maxTries) {
    throw "Postgres no respondió"
}

# --------------------------------------------------
# Liquibase
# --------------------------------------------------
Write-Host "Ejecutando Liquibase"

Ensure-PostgresDatabase `
    -Context $Context

& "$OrcRoot\commands\liquibase.ps1" `
    -Context $Context `
    -Args    @("update")
# --------------------------------------------------
# Build Django image 
# --------------------------------------------------
Write-Host "Construyendo imagen Django"

Write-Host "Esto hay en dockerConfig"
$dockerConfig | Format-List *

Invoke-OrcDocker `
    -Context $Context `
    -Args @(
        "build",
        "-t", $dockerConfig.Django.Image,
        "-f", $dockerConfig.Django.Dockerfile,
        $dockerConfig.Django.BuildContext
    )

# --------------------------------------------------
# Django
# --------------------------------------------------
Write-Host "Levantando Django"

Ensure-DockerContainerAbsent `
    -Name $dockerConfig.Django.Name

$djangoArgs = @(
    "run", "-d",
    "--name", $dockerConfig.Django.Name,
    "--network", $networkName,
    "-p", $dockerConfig.Django.Ports[0],
    "-e", "DJANGO_SETTINGS_MODULE=$projectName.settings",
    "-e", "BACKEND_DIR=/app"
)

foreach ($k in $dockerConfig.Django.Env.Keys) {
    $djangoArgs += @("-e", "$k=$($dockerConfig.Django.Env[$k])")
}

foreach ($v in $dockerConfig.Django.Volumes) {
    $djangoArgs += @("-v", "$($v.HostPath):$($v.ContainerPath)")
}

$djangoArgs += $dockerConfig.Django.Image

Invoke-OrcDocker `
    -Context $Context `
    -Args $djangoArgs

# --------------------------------------------------
# Done
# --------------------------------------------------
Write-Host ""
Write-Host "Proyecto '$projectName' levantado"
Write-Host "Backend: http://localhost:$($projectModel.Backend.Port)"

exit 0
