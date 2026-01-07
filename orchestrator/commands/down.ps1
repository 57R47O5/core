param (
    # Contexto del orco
    [Parameter(Mandatory)]
    [string]$RepoRoot,

    [Parameter(Mandatory)]
    [string]$OrcRoot,

    # Argumentos posicionales del comando
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

if ($Args.Count -lt 1) {
    Write-Host "Falta el nombre del proyecto"
    Write-Host "   Uso: orc down <nombre-proyecto>"
    exit 1
}

$project = $Args[0]

Write-Host "Deteniendo proyecto '$project'"

# ---- Backend ----
Write-Host "Deteniendo backend (manage.py runserver)"

Get-CimInstance Win32_Process |
    Where-Object {
        $_.CommandLine -match "manage.py runserver"
    } |
    ForEach-Object {
        Write-Host "  ✖ Matando PID $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force
    }

# ---- Frontend ----
Write-Host "Deteniendo frontend (npm / vite)"

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
Write-Host "Proyecto '$project' detenido"

exit 0