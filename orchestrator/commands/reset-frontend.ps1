param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$project      = $projectModel.Project
$ProjectName  = $project.Name
$FrontendPath = $projectModel.Project.FrontendPath

if (!(Test-Path $FrontendPath)) {
    Write-Host "Frontend del proyecto '$ProjectName' no existe"
    exit 1
}

Write-Host "Reseteando frontend del proyecto '$ProjectName'"
Write-Host "$FrontendPath"

$nodeModules = Join-Path $FrontendPath "node_modules"
$lockFile = Join-Path $FrontendPath "package-lock.json"

if (Test-Path $nodeModules) {
    Write-Host "Eliminando node_modules"
    Remove-Item -Recurse -Force $nodeModules
}

if (Test-Path $lockFile) {
    Write-Host "Eliminando package-lock.json"
    Remove-Item -Force $lockFile
}

Write-Host "Reinstalando dependencias"
Push-Location $FrontendPath
npm install
Pop-Location

Write-Host "Frontend '$ProjectName' reseteado correctamente"
exit 0