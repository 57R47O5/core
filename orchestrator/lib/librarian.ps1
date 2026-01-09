function Get-OrcProjectSpec {
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot,

        [Parameter(Mandatory)]
        [string]$Project
    )

    return @{
        Name = $Project

        # Paths lógicos, relativos al repo root
        ExpectedPaths = @{
            backend  = "backend/projects/$Project"
            frontend = "frontend/proyectos/$Project"
            liquibase = "docker/liquibase/changelog/projects/$Project"
        }
    }
}

function Get-OrcRegistryPath {
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot
    )

    Join-Path $RepoRoot "orchestrator/registry/registry.json"
}

function New-OrcRegistry {
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot
    )

    $backendProjects = Join-Path $RepoRoot "backend/projects"
    $backendApps     = Join-Path $RepoRoot "backend/apps"
    $registryDir     = Join-Path $RepoRoot "orchestrator/registry"
    $registryPath    = Get-OrcRegistryPath -RepoRoot $RepoRoot

    if (!(Test-Path $backendProjects)) {
        throw "No existe backend/projects"
    }

    if (!(Test-Path $backendApps)) {
        throw "No existe backend/apps"
    }

    if (!(Test-Path $registryDir)) {
        New-Item -ItemType Directory -Path $registryDir | Out-Null
    }

    $apps = Get-ChildItem $backendApps -Directory | Select-Object -ExpandProperty Name
    $projects = @{}

    foreach ($projectDir in Get-ChildItem $backendProjects -Directory) {
        $projectName = $projectDir.Name
        $settingsPy  = Join-Path $projectDir.FullName "$projectName/settings.py"

        $usedApps = @()

        if (Test-Path $settingsPy) {
            $content = Get-Content $settingsPy -Raw
            foreach ($app in $apps) {
                if ($content -match "'apps\.$app'") {
                    $usedApps += $app
                }
            }
        }

        $projects[$projectName] = @{
            apps = $usedApps
        }
    }

    $registry = @{
        projects = $projects
    }

    $registry | ConvertTo-Json -Depth 5 |
        Set-Content -Path $registryPath -Encoding UTF8

    $registry
}

function Get-OrcRegistry {
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot
    )

    $registryPath = Get-OrcRegistryPath -RepoRoot $RepoRoot

    if (!(Test-Path $registryPath)) {
        throw "Registry no encontrado en $registryPath"
    }

    try {
        Get-Content $registryPath -Raw | ConvertFrom-Json
    }
    catch {
        throw "Registry inválido (JSON mal formado)"
    }
}

function Test-OrcProjectAgainstSpec {
    param(
        [Parameter(Mandatory)]
        [string]$Project,

        [Parameter(Mandatory)]
        [string]$RepoRoot
    )

    $spec = Get-OrcProjectSpec -Project $Project

    $checks = @{}
    $ok = $true

    foreach ($key in $spec.ExpectedPaths.Keys) {
        $relative = $spec.ExpectedPaths[$key]
        $full     = Join-Path $RepoRoot $relative
        $exists   = Test-Path $full

        $checks[$key] = @{
            Path   = $relative
            Exists = $exists
        }

        if (-not $exists) {
            $ok = $false
        }
    }

    @{
        Project  = $Project
        IsValid  = $ok
        Checks   = $checks
    }
}

function Test-OrcRegistry {
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot
    )

    try {
        $registry = Get-OrcRegistry -RepoRoot $RepoRoot
    }
    catch {
        return @{
            Exists  = $false
            IsValid = $false
            Error   = $_.Exception.Message
        }
    }

    if (-not $registry.projects) {
        return @{
            Exists  = $true
            IsValid = $false
            Error   = "Falta nodo 'projects'"
        }
    }

    $projects = @{}
    $allValid = $true

    foreach ($p in $registry.projects.PSObject.Properties) {
        $hasApps = $p.Value.PSObject.Properties.Name -contains "apps"
        $isValid = $hasApps -and ($p.Value.apps -is [System.Collections.IEnumerable])

        if (-not $isValid) {
            $allValid = $false
        }

        $projects[$p.Name] = @{
            HasAppsArray = $hasApps
            AppsCount    = @($p.Value.apps).Count
            IsValid      = $isValid
        }
    }

    @{
        Exists       = $true
        IsValid      = $allValid
        ProjectCount = $projects.Count
        Projects     = $projects
    }
}

function Sync-OrcRegistry {
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot,

        [switch]$Write
    )

    $old = $null
    try { $old = Get-OrcRegistry -RepoRoot $RepoRoot } catch {}

    $new = New-OrcRegistry -RepoRoot $RepoRoot

    if (-not $old) {
        return @{ Action = "created" }
    }

    $oldP = $old.projects.PSObject.Properties.Name
    $newP = $new.projects.PSObject.Properties.Name

    @{
        Action  = "updated"
        Added   = $newP | Where-Object { $_ -notin $oldP }
        Removed = $oldP | Where-Object { $_ -notin $newP }
    }
}

function Test-OrcProjectAgainstRegistry {
    param(
        [Parameter(Mandatory)]
        [string]$Project,

        [Parameter(Mandatory)]
        [string]$RepoRoot
    )

    $registry = Get-OrcRegistry -RepoRoot $RepoRoot

    if (-not $registry.projects.$Project) {
        return @{
            Project = $Project
            IsValid = $false
            Errors  = @("Proyecto no existe en el registry")
        }
    }

    $errors   = @()
    $warnings = @()

    $backend  = Join-Path $RepoRoot "backend/projects/$Project"
    $frontend = Join-Path $RepoRoot "frontend/proyectos/$Project"

    if (!(Test-Path $backend)) {
        $errors += "Backend no existe"
    }

    if (!(Test-Path $frontend)) {
        $warnings += "Frontend no existe"
    }

    $appsRoot = Join-Path $RepoRoot "backend/apps"
    foreach ($app in $registry.projects.$Project.apps) {
        if (!(Test-Path (Join-Path $appsRoot $app))) {
            $errors += "App '$app' no existe"
        }
    }

    @{
        Project  = $Project
        IsValid  = ($errors.Count -eq 0)
        Errors   = $errors
        Warnings = $warnings
    }
}

function Show-OrcProjects {
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot
    )

    $registry = Get-OrcRegistry -RepoRoot $RepoRoot
    $registry.projects.PSObject.Properties.Name
}



