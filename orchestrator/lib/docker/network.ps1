function Ensure-GlobalNetwork {
    param ($Config)

    $networkName = $Config.GlobalNetwork

    $networks = & docker network ls --format '{{.Name}}'

    if (-not ($networks | Where-Object { $_ -eq $networkName })) {
        Write-Host "[orc] creating docker network '$networkName'"
        docker network create $networkName | Out-Null
    }
}
