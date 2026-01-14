param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$OrcScriptRoot = Split-Path $PSScriptRoot -Parent
. "$OrcScriptRoot\core\contextualizer.ps1"
. "$OrcScriptRoot\core\orc-apps.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args

$projectModel = $Context.ProjectModel
$apps = Get-OrcInstalledApps -ProjectModel $projectModel

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
