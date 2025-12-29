from pathlib import Path
import yaml
import sys


# ------------------------------------------------------------
# Paths base
# ------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
LIQUIBASE_DIR = SCRIPT_DIR.parent
CHANGELOG_ROOT = LIQUIBASE_DIR / "changelog"

REGISTRY_FILE = CHANGELOG_ROOT / "registry.yml"
GENERATED_DIR = CHANGELOG_ROOT / "generated"


# ------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------

def fail(msg: str):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def load_registry(path: Path) -> dict:
    if not path.exists():
        fail(f"No se encontró registry.yml en {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        fail(f"registry.yml inválido: {e}")

    if not data:
        fail("registry.yml está vacío")

    return data



def validate_changelog_yaml(absolute_path: Path):
    """
    Valida que un archivo changelog.yaml:
    - exista
    - sea YAML válido
    - tenga databaseChangeLog como lista
    """
    if not absolute_path.exists():
        fail(f"Changelog no encontrado: {absolute_path}")

    try:
        with absolute_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        fail(f"YAML inválido en {absolute_path}: {e}")

    if data is None:
        fail(f"El archivo {absolute_path} está vacío")

    if "databaseChangeLog" not in data:
        fail(f"{absolute_path} no define 'databaseChangeLog'")

    if not isinstance(data["databaseChangeLog"], list):
        fail(f"'databaseChangeLog' en {absolute_path} debe ser una lista")


# ------------------------------------------------------------
# Generación del master
# ------------------------------------------------------------

def include(relative_changelog_path: Path, master: dict):
    """
    Agrega un include al master.yaml y valida el changelog apuntado.

    - relative_changelog_path es relativo a CHANGELOG_ROOT
      (ej: apps/base/changelog.yaml)

    - El path escrito en el master.yaml debe ser relativo al working_dir
      de Liquibase (/workspace), por lo que se prefija con 'changelog/'.
    """
    absolute_path = CHANGELOG_ROOT / relative_changelog_path
    validate_changelog_yaml(absolute_path)

    liquibase_path = Path("changelog") / relative_changelog_path

    master["databaseChangeLog"].append({
        "include": {
            "file": liquibase_path.as_posix()
        }
    })



def generate_master(project: str, apps: list[str]):
    print(f"🔧 Generando master.yaml para proyecto '{project}'")

    if "base" not in apps:
        fail(f"El proyecto '{project}' debe incluir la app obligatoria 'base'")

    project_dir = GENERATED_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)

    master = {"databaseChangeLog": []}

    # 1️⃣ Base (siempre primero)
    include(Path("apps/base/changelog.yaml"), master)

    # 2️⃣ Apps externas
    for app in apps:
        if app == "base":
            continue

        include(Path(f"apps/{app}/changelog.yaml"), master)

    # 3️⃣ Proyecto
    include(Path(f"projects/{project}/changelog.yaml"), master)

    output_file = project_dir / "master.yaml"
    with output_file.open("w", encoding="utf-8") as f:
        yaml.dump(master, f, sort_keys=False)

    print(f"✔ {output_file.relative_to(CHANGELOG_ROOT)} generado")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    """
    Punto de entrada del generador de master changelogs.

    Uso:
        python generate_master_changelogs.py /ruta/al/registry.yml

    Responsabilidad:
    - Leer el archivo registry.yml provisto por el orquestador
    - Validar la definición de proyectos y apps
    - Generar un master.yaml por proyecto en:
        liquibase/changelog/generated/<project>/master.yaml

    Notas importantes:
    - Liquibase NO conoce ni interpreta registry.yml
    - registry.yml es una herramienta exclusiva del orquestador
    - Este script actúa como puente entre orquestación y Liquibase

    El script fallará explícitamente si:
    - No se provee la ruta al registry.yml
    - El archivo no existe o es inválido
    - Un proyecto no define apps
    """

    if len(sys.argv) != 2:
        fail(
            "Uso incorrecto.\n"
            "Ejemplo:\n"
            "  python generate_master_changelogs.py /ruta/al/registry.yml"
        )

    registry_path = Path(sys.argv[1]).resolve()

    registry = load_registry(registry_path)

    projects = registry.get("projects")
    if not projects:
        fail("registry.yml no define proyectos")

    GENERATED_DIR.mkdir(exist_ok=True)

    for project, config in projects.items():
        apps = config.get("apps")
        if not apps:
            fail(f"El proyecto '{project}' no tiene apps definidas")

        generate_master(project, apps)



if __name__ == "__main__":
    main()
