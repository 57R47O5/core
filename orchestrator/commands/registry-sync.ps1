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

$project = Resolve-OrcProject `
    -RepoRoot $RepoRoot `
    -Args     $Args `
    -Required

. "$PSScriptRoot\..\lib\librarian.ps1"

Write-Host "Orc registry sync"
Write-Host ""

$result = Sync-OrcRegistry -RepoRoot $RepoRoot -Write

switch ($result.Action) {
    "created" {
        Write-Host "Registry creado"
    }
    "updated" {
        Write-Host "Registry actualizado"
    }
    "unchanged" {
        Write-Host "Registry ya estaba en sync"
    }
}

if ($result.IsDirty) {
    Write-Host ""
    Write-Host "Cambios aplicados:"

    if ($result.Changes.AddedProjects.Count -gt 0) {
        Write-Host "Agregados:"
        $result.Changes.AddedProjects | ForEach-Object { Write-Host "  - $_" }
    }

    if ($result.Changes.RemovedProjects.Count -gt 0) {
        Write-Host "Removidos:"
        $result.Changes.RemovedProjects | ForEach-Object { Write-Host "  - $_" }
    }

    if ($result.Changes.UpdatedProjects.Count -gt 0) {
        Write-Host "Actualizados:"
        $result.Changes.UpdatedProjects | ForEach-Object { Write-Host "  - $_" }
    }
}

exit 0
