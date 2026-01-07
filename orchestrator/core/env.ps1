function New-OrcEnvFile {
    param (
        [Parameter(Mandatory)]
        $ctx,

        [Parameter(Mandatory)]
        [string]$BackendPath
    )

    $db = $ctx.Runtime.Database

    $env = @(
        "DJANGO_SECRET_KEY=unsafe-dev-key",
        "DJANGO_DEBUG=true",
        "DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1",

        "DB_ENGINE=django.db.backends.postgresql",
        "DB_NAME=$($db.Name)",
        "DB_USER=$($db.User)",
        "DB_PASSWORD=$($db.Password)",
        "DB_HOST=$($db.Host)",
        "DB_PORT=$($db.Port)",

        "CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000",
        "CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000"
    )

    $envPath = Join-Path $BackendPath ".env"

    $env | Set-Content -Path $envPath -Encoding UTF8

    Write-Host ".env generado en $envPath"
}
