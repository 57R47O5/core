function Ensure-Network {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Context
    )

    $networkName = $Context.Docker.NetworkName

    Write-Host "🌐 Verificando network '$networkName'..."

    docker network inspect $networkName *> $null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Network '$networkName' ya existe"
        return
    }

    Write-Host "⚠️  Network '$networkName' no existe. Creándola..."

    docker network create $networkName | Out-Null

    if ($LASTEXITCODE -ne 0) {
        throw "❌ No se pudo crear la network '$networkName'"
    }

    Write-Host "✅ Network '$networkName' creada correctamente"
}
