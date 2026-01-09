param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$runtime  = $Context.Runtime
$orcRoot  = $Context.OrcRoot
$repoRoot = $Context.RepoRoot
$project  = $runtime.Project

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