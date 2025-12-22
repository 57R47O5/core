import os
import shutil
import sys
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def ask_project_name():
    project_name = input("🧨 Nombre del proyecto a desmontar: ").strip().lower()

    forbidden = {"backend", "apps", "base", "scripts"}
    if project_name in forbidden:
        print("❌ No se puede desmontar un proyecto base")
        sys.exit(1)

    return project_name


def project_exists(project_name):
    return os.path.isdir(os.path.join(BASE_DIR, project_name))


def confirm_destruction(project_name):
    print("\n⚠️ ATENCIÓN ⚠️")
    print(f"Se eliminará COMPLETAMENTE el proyecto '{project_name}':")
    print(" - Carpeta del proyecto")
    print(" - Entorno virtual (.venv)")
    print(" - Schema PostgreSQL")
    print(" - Migraciones y datos\n")

    confirm = input("Escriba 'YES' para continuar: ")
    if confirm != "YES":
        print("❌ Operación cancelada")
        sys.exit(0)


def remove_project_directory(project_name):
    path = os.path.join(BASE_DIR, project_name)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"🗑️ Proyecto '{project_name}' eliminado del filesystem")


def drop_postgres_schema(schema_name):
    try:
        import psycopg2  # type: ignore

        conn = psycopg2.connect(
            dbname="monorepo",  # o postgres
            user="postgres",
            password="142857",
            host="localhost",
            port="5433",
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE;')

        cur.close()
        conn.close()

        print(f"🗑️ Schema '{schema_name}' eliminado")

    except Exception as e:
        print(f"⚠️ Error eliminando schema: {e}")

def unregister_project_from_liquibase(project_name: str):
    """
    Elimina el registro del proyecto en Liquibase:
    - Quita el include del master
    - Borra el changelog del proyecto
    """
    liquibase_dir = Path("liquibase")
    projects_dir = liquibase_dir / "changelog" / "projects"
    master_file = liquibase_dir / "changelog" / "db.changelog-master.yaml"

    project_changelog = projects_dir / f"{project_name}.yaml"

    # 1. Eliminar changelog del proyecto
    if project_changelog.exists():
        project_changelog.unlink()

    # 2. Quitar include del master
    if master_file.exists():
        lines = master_file.read_text(encoding="utf8").splitlines()
        new_lines = []

        skip = False
        for line in lines:
            if f"projects/{project_name}.yaml" in line:
                skip = True
                continue
            if skip and line.strip().startswith("file:"):
                skip = False
                continue
            if not skip:
                new_lines.append(line)

        master_file.write_text("\n".join(new_lines) + "\n", encoding="utf8")


def main():
    print("\n=== Desmontador de proyectos Django ===\n")

    project_name = ask_project_name()

    if not project_exists(project_name):
        print(f"❌ El proyecto '{project_name}' no existe")
        sys.exit(1)

    confirm_destruction(project_name)

    remove_project_directory(project_name)
    drop_postgres_schema(project_name)
    unregister_project_from_liquibase(project_name)

    print("\n✅ Proyecto desmontado correctamente")


if __name__ == "__main__":
    main()
