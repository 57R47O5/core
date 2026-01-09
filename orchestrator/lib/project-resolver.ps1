function Resolve-OrcProject {
    param (
        # Contexto explícito
        [Parameter(Mandatory)]
        [string]$RepoRoot,

        # Argumentos del comando (ej: ["my-project", "other", "flags"])
        [Parameter(Mandatory)]
        [string[]]$Args,

        # Indica si el proyecto es obligatorio para el comando
        [switch]$Required
    )

    if (-not $Args -or $Args.Count -eq 0) {
        if ($Required) {
            throw "[orc] Debe especificar un proyecto"
        }
        return $null
    }

    $projectName = $Args[0]

    $spec = Get-OrcProjectSpec `
        -RepoRoot $RepoRoot `
        -Project  $projectName

    if (-not $spec) {
        throw "[orc] Proyecto no definido: $projectName"
    }

    $result = @{
        Name         = $projectName
        RepoRoot     = $RepoRoot
        ProjectRoot  = $null
        BackendPath  = $null
        FrontendPath = $null
        Type         = @()
        Spec         = $spec
    }

    foreach ($type in $spec.ExpectedPaths.Keys) {
        $relativePath = $spec.ExpectedPaths[$type]
        $absolutePath = Join-Path $RepoRoot $relativePath

        if (Test-Path $absolutePath) {
            switch ($type) {
                "backend" {
                    $result.BackendPath = $absolutePath
                }
                "frontend" {
                    $result.FrontendPath = $absolutePath
                }
                "liquibase" {
                    $result.LiquibasePath = $absolutePath
                }
            }

            $result.Type += $type

            if (-not $result.ProjectRoot) {
                $result.ProjectRoot = Split-Path $absolutePath -Parent
            }
        }
    }

    if ($result.Type.Count -eq 0) {
        throw "[orc] Proyecto '$projectName' definido pero no presente en el filesystem"
    }

    return $result
}
