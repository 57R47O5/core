param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)


if (-not $Args -or $Args.Count -eq 0) {
    Write-Error "orc create-app: missing app name"
    exit 1
}

$appName = $Args[0]

Write-Host "orc create-app"
Write-Host "App to create: $appName"
