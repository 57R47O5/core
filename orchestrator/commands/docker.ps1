param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

Write-Host "[orc] docker $($Args -join ' ')"

& docker @Args

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
