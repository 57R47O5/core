param (
    [Parameter(Mandatory = $true)]
    [string]$RepoRoot
)

. "$PSScriptRoot\..\lib\librarian.ps1"

Write-Host "Orc registry status"
Write-Host ""

$result = Sync-OrcRegistry -RepoRoot $RepoRoot

if ($result.Action -eq "created") {
    Write-Host "Registry no existía"
}

if (-not $result.IsDirty) {
    Write-Host "Registry en sync"
    exit 0
}

Write-Host "Registry fuera de sync"
Write-Host ""

if ($result.Changes.AddedProjects.Count -gt 0) {
    Write-Host "Proyectos nuevos:"
    $result.Changes.AddedProjects | ForEach-Object { Write-Host "  - $_" }
}

if ($result.Changes.RemovedProjects.Count -gt 0) {
    Write-Host "Proyectos removidos:"
    $result.Changes.RemovedProjects | ForEach-Object { Write-Host "  - $_" }
}

if ($result.Changes.UpdatedProjects.Count -gt 0) {
    Write-Host "Proyectos modificados:"
    $result.Changes.UpdatedProjects | ForEach-Object { Write-Host "  - $_" }
}

exit 1
