function New-OrcContext {
    param (
        [Parameter(Mandatory)]
        $RuntimeConfig,

        [Parameter(Mandatory)]
        $ProjectConfig,

        [Parameter(Mandatory)]
        $Paths
    )

    return @{
        Runtime = $RuntimeConfig
        Project = $ProjectConfig
        Paths   = $Paths
    }
}
