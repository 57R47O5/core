import importlib.util
from pathlib import Path


def get_orc_apps(project_root: Path) -> list[str]:
    """
    Descubre las apps del orco a partir de:
    <project_root>/backend/config/settings/orc_apps.py
    """

    settings_path = project_root

    if not settings_path.exists():
        raise FileNotFoundError(
            f"No se encontró orc_apps.py en {settings_path}"
        )

    spec = importlib.util.spec_from_file_location("orc_apps", settings_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    raw_apps = getattr(module, "ORC_APPS", [])

    apps: list[str] = []
    for app in raw_apps:
        # Normalización del nombre lógico de la app
        apps.append(app.split(".")[-1])

    return apps


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: inspect_orc_apps.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    workspace_root = Path.cwd()
    project_root = workspace_root / project_name

    apps = get_orc_apps(project_root)

    for app in apps:
        print(app)
