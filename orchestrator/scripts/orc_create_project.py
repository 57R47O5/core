import subprocess
from pathlib import Path
import yaml
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "orchestrator" / "scripts" / "generador_proyectos.py"
ORC_YAML = REPO_ROOT / "orchestrator" / "orc.yaml"


def main(project_name: str):
    print("🐗 Helper orc_create_project iniciado")

    if not ORC_YAML.exists():
        print("❌ No se encontró orc.yaml")
        sys.exit(1)

    with ORC_YAML.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    backend_cfg = cfg.get("backend", {})
    frontend_cfg = cfg.get("frontend", {})

    enable_backend = backend_cfg.get("enabled", True)
    enable_frontend = frontend_cfg.get("enabled", True)

    cmd = [
        sys.executable,
        str(GENERATOR),
        "--project", project_name,
    ]

    if enable_backend:
        cmd.append("--backend")

    if enable_frontend:
        cmd.append("--frontend")

    print("→ Ejecutando generador (modo create):")
    print(" ".join(cmd))

    subprocess.run(cmd, check=True)

    print("✅ Proyecto creado (no construido)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python orc_create_project.py <project>")
        sys.exit(1)

    main(sys.argv[1])
