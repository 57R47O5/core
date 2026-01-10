function New-DatabaseModel {
    param (
        [Parameter(Mandatory)]
        [hashtable]$Config
    )

    return @{
        Name        = $Config.Name
        Engine      = $Config.Engine
        Host        = $Config.Host
        Port        = $Config.Port
        User        = $Config.User
        Password    = $Config.Password
        NetworkName = $Config.NetworkName
    }
}
