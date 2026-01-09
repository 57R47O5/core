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

Write-Host "[orc] docker $($Args -join ' ')"

& docker @Args

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
