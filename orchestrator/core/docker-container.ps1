function Ensure-DockerContainerAbsent {
    param (
        [Parameter(Mandatory = $true)]
        [string] $Name
    )

    docker inspect $Name *> $null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "🧹 Contenedor '$Name' existente encontrado. Eliminando..."

        docker stop $Name | Out-Null
        docker rm   $Name | Out-Null
    }
}
