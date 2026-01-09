param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$project      = $projectModel.Project
$ProjectName  = $project.Name

    Write-Host ""
    Write-Host "ORC DOCTOR - $ProjectName"
    Write-Host "============================="

    if ($Context.BackendPath) {
        Write-Host "🔎 Backend encontrado en $($Context.BackendPath)"
    }

    if ($Context.FrontendPath) {
        Write-Host "🔎 Frontend encontrado en $($Context.FrontendPath)"
    }

    $composePath = Join-Path $projectPath "docker-compose.yml"
    $envPath     = Join-Path $projectPath ".env"

    # 1. Proyecto existe
    if (-not (Test-Path $projectPath)) {
        Write-Host "Proyecto no encontrado: $projectPath"
        return
    }
    Write-Host "Proyecto encontrado"

    # 2. Docker instalado
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "Docker no está instalado"
        return
    }
    Write-Host "Docker instalado"

    # 3. Docker daemon activo
    try {
        docker info > $null 2>&1
        Write-Host "Docker daemon activo"
    } catch {
        Write-Host "Docker daemon no está corriendo"
        return
    }

    # 4. docker-compose.yml
    if (-not (Test-Path $composePath)) {
        Write-Host "docker-compose.yml no encontrado"
        return
    }
    Write-Host "docker-compose.yml presente"

    # 5. .env
    if (-not (Test-Path $envPath)) {
        Write-Host ".env no encontrado (puede ser válido)"
    } else {
        Write-Host ".env presente"
    }

    # 6. Contenedores del proyecto
    $containers = docker ps -a --filter "name=$ProjectName" --format "{{.Names}}"

    if (-not $containers) {
        Write-Host "No hay contenedores creados para este proyecto"
    } else {
        Write-Host "Contenedores detectados:"
        $containers | ForEach-Object { Write-Host "   - $_" }
    }

    # 7. Contenedores corriendo
    $running = docker ps --filter "name=$ProjectName" --format "{{.Names}}"

    if ($running) {
        Write-Host "Contenedores corriendo:"
        $running | ForEach-Object { Write-Host "   $_" }
    } else {
        Write-Host "No hay contenedores corriendo"
    }

    Write-Host ""
    Write-Host "Diagnóstico finalizado"
}
