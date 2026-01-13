param (
    [Parameter(Mandatory)]
    [hashtable]$Context,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$projectModel = $Context.ProjectModel
$project      = $projectModel.Project
$ProjectName  = $project.Name
$db = $projectModel.Database

if (-not $db) {
    throw "El proyecto '$ProjectName' no define configuración de base de datos"
}


switch ($db.Engine) {
    "django.db.backends.postgresql" {
        if (-not $db.Host -or -not $db.Name -or -not $db.User) {
            throw "Configuración de Postgres incompleta para el proyecto '$ProjectName'"
        }

        $ost = $db.Host
        $port = $db.Port
        $name = $db.Name
        $user = $db.User
        $pass = $db.Password


        Write-Host "port es $port"
        if ($pass) {
            "postgresql://${user}:${pass}@${ost}:${port}/${name}"
        }
        else {
            "postgresql://${user}@${ost}:${port}/${name}"
        }
    }

    default {
        throw "Motor de base de datos no soportado: $($db.Engine)"
    }
}
