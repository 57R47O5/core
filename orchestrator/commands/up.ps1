param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

. "$OrcScriptRoot\core\contextualizer.ps1"

$Context = Resolve-OrcContext `
    -Required $true `
    -Args    $Args
    
$projectModel = $Context.ProjectModel
$OrcRoot = $Context.OrcRoot
$project      = $projectModel.Project
$projectName  = $project.Name
$backendPath = $projectModel.Project.BackendPath
$frontendPath = $projectModel.Project.FrontendPath
$frontendBaseDir = Resolve-Path (
    Join-Path $frontendPath "..\.."
)


Write-Host "Levantando proyecto '$projectName'"
Write-Host ""
# ==================================================
# Frontend
# ==================================================

function Initialize-FrontendRuntimeRoutes {
    param (
        [Parameter(Mandatory)]
        [string]$FrontendBaseDir,

        [Parameter(Mandatory)]
        [string[]]$Apps
    )

    $srcPath     = Join-Path $FrontendBaseDir "src"
    $runtimePath = Join-Path $srcPath "runtime"

    Write-Host "Estamos en initialize... etc"
    Write-Host "runtimePath es  $runtimePath"

    if (!(Test-Path $runtimePath)) {
        New-Item -ItemType Directory -Path $runtimePath | Out-Null
    }

    $imports = @()
    $routes  = @()

    foreach ($app in $Apps) {
        $imports += "import ${app}Routes from `"../apps/$app/routes/${app}Routes`";"
        $routes  += "${app}Routes,"
    }

    $content = @"
$($imports -join "`n")

export default [
  ...
  $($routes -join ",`n  ")
];
"@

    Set-Content `
        -Path (Join-Path $runtimePath "routes.jsx") `
        -Value $content `
        -Encoding UTF8

    Write-Host "runtime/routes.jsx generado"
}


if ($frontendPath -and (Test-Path $frontendPath)) {

    $nodeModules = Join-Path $frontendBaseDir "node_modules"

    if (!(Test-Path $nodeModules)) {
        Write-Host "Frontend no construido (node_modules inexistente)"
        Write-Host "   Ejecutá: orc build $projectName"
        exit 1
    }

    Write-Host "Levantando frontend"

    $npmCmd = "npm.cmd"

    Push-Location $frontendBaseDir

    Start-Process `
    -FilePath "powershell.exe" `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "cd '$frontendBaseDir'; npm run dev"
    )

    Pop-Location
}
else {
    Write-Host "Frontend no configurado para este proyecto"
}

# ==================================================
# Backend (Django)
# ==================================================

if ($backendPath -and (Test-Path $backendPath)) {

    $installedApps = @("base")  # mínimo
    Initialize-FrontendRuntimeRoutes `
    -FrontendBaseDir $frontendBaseDir `
    -Apps $installedApps

    $venvPath    = Join-Path $backendPath ".venv"
    $pythonExe   = Join-Path $venvPath "Scripts\python.exe"

    . "$OrcRoot\core\env.ps1" 
    New-OrcEnvFile -ctx $Context

    if (!(Test-Path $pythonExe)) {
        Write-Host "❌ Backend no construido (.venv inexistente)"
        Write-Host "   Ejecutá: orc build $projectName"
        exit 1
    }

    Write-Host "🐍 Levantando Django en puerto $($projectModel.Backend.Port)"

    Push-Location $backendPath

    Start-Process `
    -FilePath "powershell.exe" `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "& `"$pythonExe`" manage.py runserver 0.0.0.0:$($projectModel.Backend.Port)"
    ) `
    -WindowStyle Normal

    Pop-Location

}
else {
    Write-Host "Backend no configurado para este proyecto"
}

# ==================================================
# Done
# ==================================================

Write-Host ""
Write-Host "🚀 Proyecto '$projectName' levantado"
Write-Host "Backend : http://localhost:$($projectModel.Backend.Port)"

if ($frontendPath) {
    Write-Host "Frontend: http://localhost:3000"
}

exit 0


