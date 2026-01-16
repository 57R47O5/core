param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# --------------------------------------------------
# Validación de argumentos
# --------------------------------------------------
if (-not $Args -or $Args.Count -lt 2) {
    Write-Error "Uso: orc generate <modelo> <app>"
    exit 1
}

$modelName = $Args[0]
$appName   = $Args[1]

Write-Host "Generando changelog para $modelName ($appName)..."

# --------------------------------------------------
# Código Python (interfaz mínima)
# --------------------------------------------------
$output = python -c @'
from orchestrator.scripts.generators.changelog import generate_constant_model_changelog
import sys

SPLIT = 999999

app_name = sys.argv[1]
model_name = sys.argv[2]

schema_xml, data_xml = generate_constant_model_changelog(app_name, model_name)

print(schema_xml)
print()
print(SPLIT)
print()

if data_xml:
    print(data_xml)
'@ $appName $modelName

#---------------------------------------------------
# Separacion
# --------------------------------------------------
$schemaLines = @()
$dataLines   = @()
$inDataPart  = $false
$separator   = "999999"

foreach ($line in $output) {
    if ($line.Trim() -eq $separator) {
        $inDataPart = $true
        continue
    }

    if (-not $inDataPart) {
        $schemaLines += $line
    } else {
        $dataLines += $line
    }
}

$schemaXml = ($schemaLines -join "`n").Trim()
$dataXml   = if ($dataLines.Count -gt 0) {
    ($dataLines -join "`n").Trim()
} else {
    $null
}


# --------------------------------------------------
# Escritura (el único path que conoce PowerShell)
# --------------------------------------------------
if (-not $schemaXml) {
    Write-Error "No se generó el changelog del modelo"
    exit 1
}

$projectRoot = Get-Location
$outputDir = Join-Path $projectRoot "projects/liquibase/changelog/apps/$appName"

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# schema
$schemaFile = Join-Path $outputDir ($modelName.ToLower() + ".xml")
$schemaXml | Out-File -FilePath $schemaFile -Encoding UTF8 -Force

Write-Host "Changelog de modelo generado:"
Write-Host "  $schemaFile"

# data (opcional)
if ($dataXml) {
    $dataFile = Join-Path $outputDir ($modelName.ToLower() + "-data.xml")
    $dataXml | Out-File -FilePath $dataFile -Encoding UTF8 -Force

    Write-Host "Changelog de datos iniciales generado:"
    Write-Host "  $dataFile"
}
