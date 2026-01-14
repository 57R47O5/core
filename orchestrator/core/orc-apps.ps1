function Get-OrcInstalledApps {
    param (
        [Parameter(Mandatory)]
        [hashtable]$ProjectModel
    )

    $appsPath = $ProjectModel.Project.AppsPath

    if (-not (Test-Path $appsPath)) {
        throw "orc_apps.py no encontrado en: $appsPath"
    }

    $content = Get-Content $appsPath -Raw

    if ($content -notmatch '(?s)ORC_APPS\s*=\s*\[(.*?)\]') {
        throw "No se encontró ORC_APPS en orc_apps.py"
    }

    $appsBlock = $Matches[1]

    $apps = [regex]::Matches($appsBlock, '"([^"]+)"') |
        ForEach-Object { $_.Groups[1].Value }

    return ,$apps  # fuerza array
}
