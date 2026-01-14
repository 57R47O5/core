param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args

$projectModel = $Context.ProjectModel
$appsPath = $projectModel.Project.AppsPath

if (-not (Test-Path $appsPath)) {
    Write-Error "orc_apps.py no encontrado en: $appsPath"
    return
}

$content = Get-Content $appsPath -Raw

# Extraer el bloque ORC_APPS = [ ... ]
if ($content -notmatch '(?s)ORC_APPS\s*=\s*\[(.*?)\]') {
    Write-Error "No se encontró ORC_APPS en orc_apps.py"
    return
}

$appsBlock = $matches[1]

# Extraer strings "..."
$apps = [regex]::Matches($appsBlock, '"([^"]+)"') |
    ForEach-Object { $_.Groups[1].Value }

if ($apps.Count -eq 0) {
    Write-Host "No hay apps instaladas"
    return
}

Write-Host ""
Write-Host "Apps instaladas en el proyecto '$($projectModel.Project.Name)':"
Write-Host ""

$i = 1
foreach ($app in $apps) {
    Write-Host ("{0}. {1}" -f $i, $app)
    $i++
}

Write-Host ""
Write-Host "$($apps.Count) app(s) instaladas"
