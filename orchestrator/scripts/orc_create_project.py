import subprocess
from pathlib import Path
import yaml
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "orchestrator" / "scripts" / "generador_proyectos.py"
ORC_YAML = REPO_ROOT / "orchestrator" /  "orc.yaml"


def main(project_name: str):
    if not ORC_YAML.exists():
        raise FileNotFoundError("No se encontró orc.yaml")

    with ORC_YAML.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    backend = cfg.get("backend", {})
    frontend = cfg.get("frontend", {})
    db = backend.get("django", {}).get("database", {})

    backend_port = backend.get("port", 8000)
    frontend_port = frontend.get("port", 3000)

    cmd = [
    str(sys.executable),
    str(GENERATOR),

    "--project", str(project_name),

    "--backend",
    "--frontend",

    "--backend-port", str(backend_port),
    "--frontend-port", str(frontend_port),

    "--db-host", str(db.get("host", "localhost")),
    "--db-port", str(db.get("port", 5433)),
    "--db-name", str(project_name),
    "--db-user", str(db.get("user", "postgres")),
    "--db-password", str(db.get("password", "")),
]



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python orc_create_project.py <project>")
        sys.exit(1)

    main(sys.argv[1])
