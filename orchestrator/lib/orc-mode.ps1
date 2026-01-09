function Resolve-OrcMode {
    param (
        [Parameter(Mandatory)]
        [string[]]$Args
    )

    $hasDocker = $Args -contains "--docker"
    $hasLocal  = $Args -contains "--local"

    if ($hasDocker -and $hasLocal) {
        throw "[orc] No se puede usar --docker y --local al mismo tiempo"
    }

    if ($hasDocker) {
        return "docker"
    }

    return "local"
}
