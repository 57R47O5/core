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


Write-Host "Levantando proyecto '$projectName'"
Write-Host ""
# ==================================================
# Frontend
# ==================================================
if ($frontendPath -and (Test-Path $frontendPath)) {

    $nodeModules = Join-Path $frontendPath "node_modules"

    if (!(Test-Path $nodeModules)) {
        Write-Host "Frontend no construido (node_modules inexistente)"
        Write-Host "   Ejecutá: orc build $projectName"
        exit 1
    }

    Write-Host "Levantando frontend"

    $npmCmd = "npm.cmd"

    Push-Location $frontendPath

    Start-Process `
    -FilePath "powershell.exe" `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "cd '$frontendPath'; npm run dev"
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
