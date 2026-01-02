param (
    [Parameter(Mandatory = $true)]
    [string]$command,

    [Parameter(Mandatory = $true)]
    [string]$project
)

$scriptRoot = $PSScriptRoot
$repoRoot   = Split-Path $scriptRoot -Parent

# -----------------------------
# Validación de comando
# -----------------------------
if ($command -ne "up" -and $command -ne "down") {
    Write-Host "❌ Comando no soportado: $command"
    Write-Host "Uso:"
    Write-Host "  orc up <proyecto>"
    Write-Host "  orc down <proyecto>"
    exit 1
}

# =============================
# ORC UP
# =============================
if ($command -eq "up") {

    # ---- Backend ----
    $backendPath  = Join-Path $repoRoot "backend\projects\$project"
    $venvActivate = Join-Path $backendPath ".venv\Scripts\activate.ps1"
    $managePy     = Join-Path $backendPath "manage.py"

    if (!(Test-Path $backendPath)) {
        Write-Host "❌ Backend del proyecto '$project' no existe"
        exit 1
    }

    if (!(Test-Path $venvActivate)) {
        Write-Host "❌ No se encontró el virtualenv en $venvActivate"
        exit 1
    }

    if (!(Test-Path $managePy)) {
        Write-Host "❌ manage.py no encontrado en $backendPath"
        exit 1
    }

    Write-Host "🐗 Levantando backend ($project) en http://localhost:8000"

    Start-Process powershell `
        -ArgumentList "-NoExit", "-Command", "cd `"$backendPath`"; . `"$venvActivate`"; python manage.py runserver" `
        -WindowStyle Normal


    # ---- Frontend ----
    $frontendPath = Join-Path $repoRoot "frontend"

    if (!(Test-Path $frontendPath)) {
        Write-Host "❌ Frontend no encontrado en $frontendPath"
        exit 1
    }

    Write-Host "🐗 Levantando frontend en http://localhost:3000"

    Start-Process powershell `
        -ArgumentList "-NoExit", "-Command", "cd `"$frontendPath`"; npm run dev" `
        -WindowStyle Normal


    Write-Host ""
    Write-Host "✅ Proyecto '$project' levantado"
    Write-Host "   Backend : http://localhost:8000"
    Write-Host "   Frontend: http://localhost:3000"

    exit 0
}

# =============================
# ORC DOWN
# =============================
if ($command -eq "down") {

    Write-Host "🐗 Deteniendo proyecto '$project'"

    # ---- Backend ----
    Write-Host "🔻 Deteniendo backend (manage.py runserver)"

    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -match "manage.py runserver"
        } |
        ForEach-Object {
            Write-Host "  ✖ Matando PID $($_.ProcessId)"
            Stop-Process -Id $_.ProcessId -Force
        }

    # ---- Frontend ----
    Write-Host "🔻 Deteniendo frontend (npm / vite)"

    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -match "npm run dev" -or
            $_.CommandLine -match "vite"
        } |
        ForEach-Object {
            Write-Host "  ✖ Matando PID $($_.ProcessId)"
            Stop-Process -Id $_.ProcessId -Force
        }

    Write-Host ""
    Write-Host "✅ Proyecto '$project' detenido"

    exit 0
}
