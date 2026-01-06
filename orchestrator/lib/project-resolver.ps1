function Resolve-OrcProject {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Project
    )

    $repoRoot = Resolve-OrcRepoRoot
    $spec     = Get-OrcProjectSpec -Project $Project

    $result = @{
        Name         = $Project
        RepoRoot     = $repoRoot
        BackendPath  = $null
        FrontendPath = $null
        Type         = @()
    }

    foreach ($type in $spec.ExpectedPaths.Keys) {
        $relativePath = $spec.ExpectedPaths[$type]
        $absolutePath = Join-Path $repoRoot $relativePath

        if (Test-Path $absolutePath) {
            switch ($type) {
                "backend" {
                    $result.BackendPath = $absolutePath
                }
                "frontend" {
                    $result.FrontendPath = $absolutePath
                }
            }

            $result.Type += $type
        }
    }

    if ($result.Type.Count -eq 0) {
        throw "Proyecto '$Project' definido pero no presente en el filesystem"
    }

    return $result
}
