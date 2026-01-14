function Initialize-FrontendApps {
    param (
        [Parameter(Mandatory)]
        [string]$FrontendPath
    )

    $srcPath  = Join-Path $FrontendPath "src"
    $appsPath = Join-Path $srcPath "apps"

    if (-not (Test-Path $srcPath)) {
        throw "No se encontró src/ en el frontend"
    }

    if (-not (Test-Path $appsPath)) {
        New-Item -ItemType Directory -Path $appsPath | Out-Null
    }

    # Apps.jsx (congelado)
    $appsJsxPath = Join-Path $srcPath "Apps.jsx"
    Set-Content -Path $appsJsxPath -Value $appsJsxContent -Encoding UTF8

    # apps.registry.js (puente)
    $registryPath = Join-Path $appsPath "apps.registry.js"
    Set-Content -Path $registryPath -Value $registryContent -Encoding UTF8

    Write-Host "Apps.jsx y apps.registry.js generados correctamente"
}
