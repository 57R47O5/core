function Resolve-OrcRepoRoot {
    $scriptRoot = $PSScriptRoot
    $orcRoot    = Split-Path $scriptRoot -Parent
    return Split-Path $orcRoot -Parent
}
