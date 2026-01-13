param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel = $Context.ProjectModel
$OrcRoot = $Context.OrcRoot
$project      = $projectModel.Project
$projectName  = $project.Name
$backendPath = $projectModel.Project.BackendPath
$frontendPath = $projectModel.Project.FrontendPath


Write-Host "🐗 Levantando proyecto '$projectName'"
Write-Host ""

# ==================================================
# Backend (Django)
# ==================================================

if ($backendPath -and (Test-Path $backendPath)) {

    $venvPath    = Join-Path $backendPath ".env"
    $pythonExe   = Join-Path $venvPath "Scripts\python.exe"

    if (!(Test-Path $pythonExe)) {
        Write-Host "❌ Backend no construido (.env inexistente)"
        Write-Host "   Ejecutá: orc build $projectName"
        exit 1
    }

    Write-Host "🐍 Levantando Django en puerto $($projectModel.Backend.Port)"

    Push-Location $backendPath

    Start-Process `
        -FilePath $pythonExe `
        -ArgumentList "manage.py runserver 0.0.0.0:$($projectModel.Backend.Port)" `
        -NoNewWindow

    Pop-Location


    . "$OrcRoot\core\env.ps1" 
    New-OrcEnvFile -ctx $Context
}
else {
    Write-Host "ℹ️  Backend no configurado para este proyecto"
}

# ==================================================
# Frontend
# ==================================================

if ($frontendPath -and (Test-Path $frontendPath)) {

    $nodeModules = Join-Path $frontendPath "node_modules"

    if (!(Test-Path $nodeModules)) {
        Write-Host "❌ Frontend no construido (node_modules inexistente)"
        Write-Host "   Ejecutá: orc build $projectName"
        exit 1
    }

    Write-Host "⚛️  Levantando frontend"

    Push-Location $frontendPath

    Start-Process `
        -FilePath "npm" `
        -ArgumentList "run dev" `
        -NoNewWindow

    Pop-Location
}
else {
    Write-Host "ℹ️  Frontend no configurado para este proyecto"
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
