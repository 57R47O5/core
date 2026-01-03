param (
    [Parameter(Mandatory = $true)]
    [string]$project,

    [Parameter(Mandatory = $true)]
    [string]$repoRoot
)

$backendPath  = Join-Path $repoRoot "backend\projects\$project"
$frontendPath = Join-Path $repoRoot "frontend\proyectos\$project"

if (Test-Path $backendPath -or Test-Path $frontendPath) {
    Write-Host "El proyecto '$project' ya existe"
    exit 1
}

$generator = Join-Path $repoRoot "backend\scripts\generador_proyectos.py"

if (!(Test-Path $generator)) {
    Write-Host "No se encontró el generador en $generator"
    exit 1
}

Write-Host "Creando proyecto '$project'"

try {
    python $generator --project $project
}
catch {
    Write-Host "❌ Error creando el proyecto '$project'"
    exit 1
}

Write-Host ""
Write-Host "Proyecto '$project' creado correctamente"
Write-Host "Podés levantarlo con:"
Write-Host "  orc up $project"

exit 0
