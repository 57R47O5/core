param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel = $Context.ProjectModel
$projectName  = $projectModel.Project.Name
$OrcRoot      = $Context.OrcRoot

Write-Host "OrcRoot es $OrcRoot"

. "$OrcRoot\core\process.ps1"

Write-Host "🐗 Deteniendo proyecto '$projectName'"
Write-Host ""

# ==================================================
# Backend (Django)
# ==================================================

if ($projectModel.Backend -and $projectModel.Backend.Port) {
    $backendPort = $projectModel.Backend.Port
    Stop-ProcessByPort -Port $backendPort -Label "(backend)"
}
else {
    Write-Host "Backend no configurado"
}

# ==================================================
# Frontend (Vite)
# ==================================================

$frontendPort = 3000  # futuro: hacerlo configurable

Stop-ProcessByPort -Port $frontendPort -Label "(frontend)"

# ==================================================
# Done
# ==================================================

Write-Host ""
Write-Host "🛑 Proyecto '$projectName' detenido"
exit 0
