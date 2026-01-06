function Get-OrcProjectSpec {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Project
    )

    return @{
        Name = $Project

        # Paths lógicos, relativos al repo root
        ExpectedPaths = @{
            backend  = "backend/projects/$Project"
            frontend = "frontend/proyectos/$Project"
        }
    }
}

function New-OrcRegistry {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot
    )

    $backendProjects = Join-Path $RepoRoot "backend\projects"
    $backendApps     = Join-Path $RepoRoot "backend\apps"
    $registryDir     = Join-Path $RepoRoot "orchestrator\registry"
    $registryPath    = Join-Path $registryDir "registry.json"

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

    $projectsData = @{}

    foreach ($projectDir in Get-ChildItem $backendProjects -Directory) {
        $projectName = $projectDir.Name
        $settingsPy  = Join-Path $projectDir.FullName "$projectName\settings.py"

        $usedApps = @()

        if (Test-Path $settingsPy) {
            $content = Get-Content $settingsPy -Raw
            foreach ($app in $apps) {
                if ($content -match "'apps\.$app'") {
                    $usedApps += $app
                }
            }
        }

        $projectsData[$projectName] = @{
            apps = $usedApps
        }
    }

    $registry = @{
        projects = $projectsData
    }

    $json = $registry | ConvertTo-Json -Depth 5
    Set-Content -Path $registryPath -Value $json -Encoding UTF8

    Write-Host "Registry generado en $registryPath"
}

function Test-OrcProjectAgainstSpec {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Project,

        [Parameter(Mandatory = $true)]
        [string]$RepoRoot
    )

    $registryPath = Join-Path $RepoRoot "orchestrator\registry\registry.json"

    if (!(Test-Path $registryPath)) {
        throw "Registry no encontrado en $registryPath"
    }

    $registry = Get-Content $registryPath -Raw | ConvertFrom-Json

    $existsInRegistry = $registry.projects.PSObject.Properties.Name -contains $Project

    $spec = Get-OrcProjectSpec -Project $Project

    $pathChecks = @{}
    $allPathsOk = $true

    foreach ($key in $spec.ExpectedPaths.Keys) {
        $relativePath = $spec.ExpectedPaths[$key]
        $fullPath     = Join-Path $RepoRoot $relativePath
        $exists       = Test-Path $fullPath

        $pathChecks[$key] = @{
            expected = $relativePath
            exists   = $exists
        }

        if (-not $exists) {
            $allPathsOk = $false
        }
    }

    return @{
        Project          = $Project
        ExistsInRegistry = $existsInRegistry
        PathChecks       = $pathChecks
        IsValid          = ($existsInRegistry -and $allPathsOk)
    }
}

function Test-OrcRegistry {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot
    )

    $registryPath = Join-Path $RepoRoot "orchestrator\registry\registry.json"

    if (!(Test-Path $registryPath)) {
        return @{
            RegistryPath = $registryPath
            Exists       = $false
            IsValid      = $false
            Error        = "Registry no encontrado"
        }
    }

    try {
        $registry = Get-Content $registryPath -Raw | ConvertFrom-Json
    }
    catch {
        return @{
            RegistryPath = $registryPath
            Exists       = $true
            IsValid      = $false
            Error        = "Registry inválido (JSON mal formado)"
        }
    }

    if (-not $registry.projects) {
        return @{
            RegistryPath = $registryPath
            Exists       = $true
            IsValid      = $false
            Error        = "Falta nodo 'projects'"
        }
    }

    $projectsResult = @{}
    $allValid = $true

    foreach ($prop in $registry.projects.PSObject.Properties) {
        $projectName = $prop.Name
        $projectData = $prop.Value

        $hasAppsArray = $false
        $appsCount    = 0

        if ($projectData.PSObject.Properties.Name -contains "apps") {
            if ($projectData.apps -is [System.Collections.IEnumerable]) {
                $hasAppsArray = $true
                $appsCount    = @($projectData.apps).Count
            }
        }

        $isValid = $hasAppsArray

        if (-not $isValid) {
            $allValid = $false
        }

        $projectsResult[$projectName] = @{
            HasAppsArray = $hasAppsArray
            AppsCount    = $appsCount
            IsValid      = $isValid
        }
    }

    return @{
        RegistryPath = $registryPath
        Exists       = $true
        ProjectCount = $projectsResult.Count
        Projects     = $projectsResult
        IsValid      = $allValid
    }
}

function Sync-OrcRegistry {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot,

        [switch]$Write
    )

    $registryPath = Join-Path $RepoRoot "orchestrator\registry\registry.json"

    # 1. Snapshot actual (si existe)
    $oldRegistry = $null
    if (Test-Path $registryPath) {
        try {
            $oldRegistry = Get-Content $registryPath -Raw | ConvertFrom-Json
        } catch {
            throw "Registry existente inválido, no se puede sincronizar"
        }
    }

    # 2. Generar registry nuevo (en memoria)
    $tempPath = Join-Path $RepoRoot "orchestrator\registry\.registry.tmp.json"
    New-OrcRegistry -RepoRoot $RepoRoot
    $newRegistry = Get-Content $registryPath -Raw | ConvertFrom-Json

    # 3. Comparar
    $oldProjects = @{}
    if ($oldRegistry) {
        foreach ($p in $oldRegistry.projects.PSObject.Properties) {
            $oldProjects[$p.Name] = $p.Value
        }
    }

    $newProjects = @{}
    foreach ($p in $newRegistry.projects.PSObject.Properties) {
        $newProjects[$p.Name] = $p.Value
    }

    $added   = $newProjects.Keys | Where-Object { $_ -notin $oldProjects.Keys }
    $removed = $oldProjects.Keys | Where-Object { $_ -notin $newProjects.Keys }

    $updated = @()
    foreach ($name in ($newProjects.Keys | Where-Object { $_ -in $oldProjects.Keys })) {
        if ((ConvertTo-Json $newProjects[$name]) -ne (ConvertTo-Json $oldProjects[$name])) {
            $updated += $name
        }
    }

    $isDirty = ($added.Count + $removed.Count + $updated.Count) -gt 0

    # 4. Decidir acción
    if (-not $oldRegistry) {
        $action = "created"
    } elseif ($isDirty) {
        $action = "updated"
    } else {
        $action = "unchanged"
    }

    # 5. Escribir solo si se pide
    if ($Write -and $isDirty) {
        $json = $newRegistry | ConvertTo-Json -Depth 5
        Set-Content -Path $registryPath -Value $json -Encoding UTF8
    }

    return @{
        RegistryPath = $registryPath
        Action       = $action
        IsDirty      = $isDirty
        Changes      = @{
            AddedProjects   = $added
            RemovedProjects = $removed
            UpdatedProjects = $updated
        }
    }
}

function Test-OrcProjectAgainstRegistry {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Project,

        [Parameter(Mandatory = $true)]
        [string]$RepoRoot
    )

    $errors   = @()
    $warnings = @()

    $registryPath = Join-Path $RepoRoot "orchestrator\registry\registry.json"

    if (!(Test-Path $registryPath)) {
        throw "Registry no encontrado en $registryPath"
    }

    $registry = Get-Content $registryPath -Raw | ConvertFrom-Json

    if (-not $registry.projects.$Project) {
        return @{
            Project  = $Project
            IsValid  = $false
            Errors   = @("Proyecto '$Project' no existe en el registry")
            Warnings = @()
            Checked  = @{}
        }
    }

    $projectEntry = $registry.projects.$Project

    # Paths esperados
    $backendPath  = Join-Path $RepoRoot "backend\projects\$Project"
    $frontendPath = Join-Path $RepoRoot "frontend\proyectos\$Project"

    $checked = @{
        BackendPath  = $false
        FrontendPath = $false
        Apps         = @()
    }

    if (Test-Path $backendPath) {
        $checked.BackendPath = $true
    } else {
        $errors += "Backend no existe: backend/projects/$Project"
    }

    if (Test-Path $frontendPath) {
        $checked.FrontendPath = $true
    } else {
        $warnings += "Frontend no existe (puede ser intencional)"
    }

    # Apps
    $appsRoot = Join-Path $RepoRoot "backend\apps"

    foreach ($app in $projectEntry.apps) {
        $appPath = Join-Path $appsRoot $app
        if (Test-Path $appPath) {
            $checked.Apps += $app
        } else {
            $errors += "App '$app' no existe en backend/apps"
        }
    }

    return @{
        Project  = $Project
        IsValid  = ($errors.Count -eq 0)
        Errors   = $errors
        Warnings = $warnings
        Checked  = $checked
    }
}

function Show-OrcProjects {
    Write-Host "Proyectos registrados:"
    Write-Host ""

    try {
        $projects = Get-OrcProjects
    }
    catch {
        Write-Host "Error leyendo registry"
        Write-Host $_
        exit 1
    }

    if ($projects.Count -eq 0) {
        Write-Host " (ninguno)"
        return
    }

    foreach ($p in $projects) {
        Write-Host " - $p"
    }
}


