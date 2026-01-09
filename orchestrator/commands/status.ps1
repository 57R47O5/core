param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$project = $projectModel.Project

Write-Host ""
Write-Host "ORC STATUS - $project"
Write-Host ""

# ---------- Backend ----------

Write-Host "Backend:"

if (Test-Path $projectModel.Project.BackendPath) {
    Write-Host "  Proyecto encontrado"
} else {
    Write-Host "  Proyecto NO existe"
}

if (Test-Path $projectModel.Backend.ManagePy) {
    Write-Host "  manage.py presente"
} else {
    Write-Host "  manage.py ausente"
}

if (Test-Path $projectModel.Backend.VenvPath) {
    Write-Host "  Virtualenv presente"
} else {
    Write-Host "  Virtualenv ausente"
}

# Django corriendo?
$djangoRunning = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($djangoRunning) {
    Write-Host "  Django corriendo en http://localhost:8000"
} else {
    Write-Host "  Django NO esta corriendo"
}

Write-Host ""

# ---------- Frontend ----------
Write-Host "Frontend:"

if (Test-Path $projectModel.Project.FrontendPath) {
    Write-Host "  Proyecto frontend encontrado"
} else {
    Write-Host "  Proyecto frontend NO existe"
}

# Vite (puerto 3000 o 5173)
$vite3000 = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
$vite5173 = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue

if ($vite3000) {
    Write-Host "  Vite corriendo en http://localhost:3000"
}
elseif ($vite5173) {
    Write-Host "  Vite corriendo en http://localhost:5173"
}
else {
    Write-Host "  Vite NO esta corriendo"
}

Write-Host ""

# ---------- Estado general ----------
Write-Host "Estado general:"

if ($djangoRunning -and ($vite3000 -or $vite5173)) {
    Write-Host "  Proyecto operativo"
}
elseif ($djangoRunning -or ($vite3000 -or $vite5173)) {
    Write-Host "  Proyecto parcialmente levantado"
}
else {
    Write-Host "  Proyecto detenido"
}

Write-Host ""
exit 0
