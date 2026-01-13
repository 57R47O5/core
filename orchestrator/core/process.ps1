function Stop-ProcessByPort {
    param (
        [Parameter(Mandatory)]
        [int]$Port,

        [string]$Label = ""
    )

    $connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue

    if (!$connections) {
        Write-Host "No hay proceso escuchando en puerto $Port $Label"
        return
    }

    foreach ($conn in $connections) {
        $pid = $conn.OwningProcess
        try {
            $proc = Get-Process -Id $pid -ErrorAction Stop
            Write-Host "Deteniendo proceso PID $pid ($($proc.ProcessName)) en puerto $Port $Label"
            Stop-Process -Id $pid -Force
        }
        catch {
            Write-Host "No se pudo detener PID $pid en puerto $Port"
        }
    }
}
