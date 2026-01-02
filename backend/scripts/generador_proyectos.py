import subprocess
from pathlib import Path
import secrets
import argparse

# ==============================
# Constants
# ==============================

REPO_ROOT = Path(__file__).resolve().parents[2]

BACKEND_PROJECTS_DIR = REPO_ROOT / "backendpy" / "projects"
FRONTEND_PROJECTS_DIR = REPO_ROOT / "frontend" / "proyectos"
LIQUIBASE_ROOT = Path("docker") / "liquibase"
LIQUIBASE_PROJECTS_DIR = LIQUIBASE_ROOT / "changelog" / "projects"


# ==============================
# Helpers
# ==============================

def run(cmd, cwd=None, env=None):
    """
    Ejecuta un comando del sistema mostrando el comando por consola.
    Falla inmediatamente si el comando devuelve error.
    """
    print("→", " ".join(map(str, cmd)))
    subprocess.run(cmd, cwd=cwd, env=env, check=True)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=False)
    parser.add_argument("--backend", action="store_true")
    parser.add_argument("--frontend", action="store_true")
    return parser.parse_args()


# ==============================
# Entrada de datos
# ==============================

def ask_project_name():
    """
    Solicita al usuario el nombre del proyecto.
    """
    nombre = input("👉 Nombre del proyecto: ").strip()
    if not nombre:
        raise ValueError("El nombre del proyecto no puede estar vacío")
    return nombre


# ==============================
# Proyecto y entorno
# ==============================

def create_project_directory(project_name):
    """
    Crea el directorio del proyecto dentro de backend/.
    """
    project_dir = BACKEND_PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def create_virtualenv(project_dir):
    """
    Crea el entorno virtual usando uv.
    """
    run(["uv", "venv", ".venv"], cwd=project_dir)


def install_dependencies(project_dir):
    """
    Instala las dependencias base del proyecto.
    """
    run(
        [
            "uv",
            "pip",
            "install",
            "django",
            "psycopg2-binary",
            "python-dotenv",
            "django-cors-headers",
        ],
        cwd=project_dir,
    )


# ==============================
# Django
# ==============================

def create_django_project(project_name, project_dir):
    """
    Inicializa el proyecto Django.
    """
    run(
        ["uv", "run", "django-admin", "startproject", project_name, "."],
        cwd=project_dir,
    )


# ==============================
# Settings
# ==============================

def configure_settings(project_name, project_dir):
    """
    Ajusta settings.py para:
    - usar .env
    - soportar monorepo
    - configurar apps base
    - configurar base de datos
    """
    settings_path = project_dir / project_name / "settings.py"
    settings = settings_path.read_text()

    settings = settings.replace(
        "BASE_DIR = Path(__file__).resolve().parent.parent",
        """BASE_DIR = Path(__file__).resolve().parent.parent

import os
import sys
from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")

BACKEND_DIR = BASE_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
""",
    )

    settings = settings.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n"
        "    'corsheaders',\n"
        "    'apps.base',\n"
        "    'apps.auditoria',",
    )

    settings = settings.replace(
        "MIDDLEWARE = [",
        "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',",
    )

    settings += """
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

AUTH_USER_MODEL = 'base.User'

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True
"""

    settings_path.write_text(settings)


# ==============================
# VS Code
# ==============================

def configure_vscode(project_dir):
    """
    Crea la configuración recomendada para VS Code.
    """
    vscode_dir = project_dir / ".vscode"
    vscode_dir.mkdir(exist_ok=True)

    (vscode_dir / "settings.json").write_text(
        """{
  "python.defaultInterpreterPath": ".venv/Scripts/python.exe",
  "python.analysis.extraPaths": [
    "..",
    "../apps"
  ],
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoSearchPaths": true,
  "python.terminal.activateEnvironment": false,
  "editor.formatOnSave": true
}
""",
        encoding="utf8",
    )

    (vscode_dir / "extensions.json").write_text(
        """{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance"
  ]
}
""",
        encoding="utf8",
    )


# ==============================
# Environment & DB
# ==============================

def create_env_file(project_dir, db_name):
    """
    Genera el archivo .env del proyecto.
    """
    secret_key = secrets.token_urlsafe(50)

    (project_dir / ".env").write_text(
        f"""# DJANGO
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# DATABASE
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB={db_name}
POSTGRES_USER=postgres
POSTGRES_PASSWORD=142857
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=True
""",
        encoding="utf8",
    )


def create_postgres_schema(schema_name):
    """
    Crea un schema PostgreSQL si no existe.
    """
    try:
        import psycopg2  # type: ignore

        conn = psycopg2.connect(
            dbname="postgres",   
            user="postgres",
            password="142857",
            host="localhost",
            port="5433",
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}";')

        cur.close()
        conn.close()

        print(f"✅ Schema '{schema_name}' creado o ya existente")

    except Exception as e:
        print(f"⚠️ Error creando schema '{schema_name}': {e}")


# ==============================
# Liquibase
# ==============================

def register_project_in_liquibase(project_name: str) -> None:
    """
    Registra un nuevo proyecto en Liquibase.

    - Crea el directorio del proyecto en changelog/projects/
    - Crea un changelog inicial vacío (001-init.yaml)

    No modifica el master changelog.
    No ejecuta Liquibase.
    """
    project_dir = LIQUIBASE_PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    initial_changelog = project_dir / "001-init.yaml"

    if not initial_changelog.exists():
        initial_changelog.write_text(
            f"""databaseChangeLog:
  - comment: Changelog inicial del proyecto {project_name}
""",
            encoding="utf8",
        )

        print(f"🧩 Liquibase: proyecto '{project_name}' registrado")
    else:
        print(f"ℹ️ Liquibase: proyecto '{project_name}' ya existe")

# ==============================
# Frontend
# ==============================

def create_frontend_project(project_name):
    project_dir = FRONTEND_PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    run(["npm", "create", "vite@latest", ".", "--", "--template", "react"], cwd=project_dir)
    run(["npm", "install"], cwd=project_dir)

    return project_dir


# ==============================
# Main
# ==============================

def main():
    args = parse_args()

    if args.project:
        project_name = args.project
    else:
        project_name = ask_project_name()
    project_dir = create_project_directory(project_name)

    print(f"\n🚀 Creando proyecto '{project_name}'\n")

    if args.backend:
        create_virtualenv(project_dir)
        install_dependencies(project_dir)
        create_django_project(project_name, project_dir)
        configure_settings(project_name, project_dir)
        configure_vscode(project_dir)
        create_env_file(project_dir, project_name)
        create_postgres_schema(project_name)
        register_project_in_liquibase(project_name)
    if args.frontend:
        create_frontend_project(project_name)

    print("\n🎉 Proyecto creado correctamente")
    print("📌 El schema será gestionado por Liquibase")
    print(f"cd backend/{project_name}")
    print("uv run python manage.py runserver")


if __name__ == "__main__":
    main()
