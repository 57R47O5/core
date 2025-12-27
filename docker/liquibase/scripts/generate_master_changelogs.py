from pathlib import Path
import yaml
import sys

ROOT = Path(__file__).resolve().parents[1] / "changelog"

REGISTRY_FILE = ROOT / "registry.yml"
GENERATED_DIR = ROOT / "generated"


def fail(msg: str):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def load_registry():
    if not REGISTRY_FILE.exists():
        fail(f"No se encontró {REGISTRY_FILE}")

    with REGISTRY_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_file(path: Path):
    if not path.exists():
        fail(f"Archivo requerido no encontrado: {path}")


def generate_master(project: str, apps: list[str]):
    print(f"Generando master.yaml para proyecto '{project}'")

    project_dir = GENERATED_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)

    changelog = {"databaseChangeLog": []}

    # 1. Base (obligatorio)
    if "base" not in apps:
        fail(f"El proyecto '{project}' no incluye la app obligatoria 'base'")

    base_changelog = Path("core/base/changelog.yaml")
    validate_file(ROOT / base_changelog)

    changelog["databaseChangeLog"].append({
        "include": {"file": str(base_changelog)}
    })

    # 2. Apps externas (excepto base)
    for app in apps:
        if app == "base":
            continue

        app_changelog = Path(f"apps/{app}/changelog.yaml")
        validate_file(ROOT / app_changelog)

        changelog["databaseChangeLog"].append({
            "include": {"file": str(app_changelog)}
        })

    # 3. Proyecto
    project_changelog = Path(f"projects/{project}/changelog.yaml")
    validate_file(ROOT / project_changelog)

    changelog["databaseChangeLog"].append({
        "include": {"file": str(project_changelog)}
    })

    output_file = project_dir / "master.yaml"
    with output_file.open("w", encoding="utf-8") as f:
        yaml.dump(changelog, f, sort_keys=False)

    print(f"✔ {output_file} generado")


def main():
    registry = load_registry()

    projects = registry.get("projects")
    if not projects:
        fail("registry.yml no define proyectos")

    GENERATED_DIR.mkdir(exist_ok=True)

    for project, config in projects.items():
        apps = config.get("apps", [])
        if not apps:
            fail(f"El proyecto '{project}' no tiene apps definidas")

        generate_master(project, apps)


if __name__ == "__main__":
    main()
