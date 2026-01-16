function Invoke-ConstantModelLiquibaseGeneration {
    param (
        [Parameter(Mandatory)]
        [string]$ModelFile,

        [Parameter(Mandatory)]
        [string]$OutputFile
    )

    if (-not (Test-Path $ModelFile)) {
        throw "Model file not found: $ModelFile"
    }

    $xml = python - <<EOF
from yourmodule import generate_constant_model_changelog
print(generate_constant_model_changelog(r"$ModelFile"))
EOF

    if (-not $xml) {
        throw "No XML generated"
    }

    $xml | Out-File -FilePath $OutputFile -Encoding UTF8 -Force

    Write-Host "Liquibase changelog generado:"
    Write-Host "  $OutputFile"
}
