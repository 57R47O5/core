param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel  = $Context.ProjectModel
$project  = $projectModel.Project
$ProjectName  = $project.Name

Write-Host "Deteniendo proyecto '$ProjectName'"

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
Write-Host "Proyecto '$ProjectName' detenido"

exit 0