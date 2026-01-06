function Get-OrcProjects {
    $scriptRoot = $PSScriptRoot
    $orcRoot    = Split-Path $scriptRoot -Parent
    $registry   = Join-Path $orcRoot "registry\registry.yaml"

    if (!(Test-Path $registry)) {
        throw "Registry no encontrado en $registry"
    }

    $projects = python - << 'EOF'
import yaml, sys

registry_path = sys.argv[1]

with open(registry_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f) or {}

projects = data.get("projects", {})

for name in projects.keys():
    print(name)
EOF
    $registry

    return $projects -split "`n" | Where-Object { $_ -ne "" }
}