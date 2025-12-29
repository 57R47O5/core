from pathlib import Path
import sys
import yaml
import re


def fail(msg: str):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def info(msg: str):
    print(f"[INFO] {msg}")


def load_registry(registry_path: Path) -> dict:
    if not registry_path.exists():
        fail(f"Registry no encontrado: {registry_path}")

    try:
        with registry_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        fail(f"Registry inválido (YAML): {e}")

    if not data:
        fail("Registry vacío")

    if "projects" not in data:
        fail("Registry no define la clave 'projects'")

    return data


def read_installed_apps(settings_path: Path) -> set[str]:
    if not settings_path.exists():
        fail(f"No existe settings.py: {settings_path}")

    content = settings_path.read_text(encoding="utf-8")

    match = re.search(
        r"INSTALLED_APPS\s*=\s*\[(?P<body>[\s\S]*?)\]",
        content,
    )

    if not match:
        fail(f"No se pudo encontrar INSTALLED_APPS en {settings_path}")

    block = match.group("body")

    apps = set()

    for line in block.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        # limpiar comillas y coma
        entry = line.strip(",").strip("'\"")

        # Caso apps.<app>[.apps.Config]
        if entry.startswith("apps."):
            parts = entry.split(".")
            if len(parts) >= 2:
                apps.add(parts[1])
            continue

        # Caso app[.apps.Config]
        parts = entry.split(".")
        if len(parts) == 1:
            apps.add(parts[0])
            continue

        # todo lo demás (django.contrib.*, terceros) se ignora

    return apps



def validate_registry(registry: dict, repo_root: Path):
    backend_dir = repo_root / "backend"
    projects_dir = backend_dir / "projects"
    shared_apps_dir = backend_dir / "apps"

    if not projects_dir.exists():
        fail(f"No existe el directorio 'projects': {projects_dir}")

    for project, config in registry["projects"].items():
        info(f"Validando proyecto '{project}'")

        project_dir = projects_dir / project
        if not project_dir.exists():
            fail(f"Proyecto '{project}' no existe en filesystem: {project_dir}")

        django_project_dir = projects_dir / project / f'{project}' 
        settings_path = django_project_dir / "settings.py"

        installed_apps = read_installed_apps(settings_path)

        apps = config.get("apps")
        if not apps or not isinstance(apps, list):
            fail(f"Proyecto '{project}' no tiene apps válidas definidas")

        seen = set()
        for app in apps:
            if app in seen:
                fail(f"App duplicada '{app}' en proyecto '{project}'")
            seen.add(app)

            local_app = django_project_dir / "apps" / app
            shared_app = shared_apps_dir / app

            if not (local_app.exists() or shared_app.exists()):
                fail(
                    f"App '{app}' declarada en proyecto '{project}' "
                    f"no existe ni como app local ni compartida"
                )

            if app not in installed_apps:
                fail(
                    f"App '{app}' declarada en registry para '{project}' "
                    f"no está en INSTALLED_APPS"
                )

    info("Registry válido ✔")


def main():
    """
    Uso:
        python validate_registry.py <path_registry.yml>

    Ejemplo:
        python orchestrator/scripts/validate_registry.py orchestrator/registry/registry.yml
    """
    if len(sys.argv) != 2:
        fail("Uso: validate_registry.py <path_registry.yaml>")

    registry_path = Path(sys.argv[1]).resolve()

    # registry vive en orchestrator/registry → repo root es 2 niveles arriba
    repo_root = registry_path.parents[2]

    registry = load_registry(registry_path)
    validate_registry(registry, repo_root)


if __name__ == "__main__":
    main()
