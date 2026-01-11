param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel = $Context.ProjectModel
$projectName  = $projectModel.Project.Name
$docker       = $Context.Docker

. "$OrcRoot\config\docker.config.ps1"
. "$OrcRoot\config\liquibase.config.ps1"

Write-Host "Deteniendo proyecto '$projectName'"

$dockerConfig = Get-OrcDockerConfig -ctx $Context
$networkName  = $docker.NetworkName

# --------------------------------------------------
# Contenedores a detener (orden inverso a up)
# --------------------------------------------------
$containers = @()

if ($dockerConfig.Django) {
    $containers += "$projectName-backend"
}

if ($dockerConfig.Postgres) {
    $containers += $dockerConfig.Postgres.Name
}

foreach ($name in $containers) {
    Write-Host "Deteniendo contenedor '$name'"

    docker inspect $name *> $null
    if ($LASTEXITCODE -eq 0) {
        docker stop $name | Out-Null
        docker rm $name   | Out-Null
    } else {
        Write-Host " No existe (ok)"
    }
}

# --------------------------------------------------
# Network (opcionalmente la dejamos)
# --------------------------------------------------
Write-Host "Network '$networkName' se mantiene (orc down no destruye infra)"

Write-Host ""
Write-Host "Proyecto '$projectName' detenido"

exit 0
