import subprocess
from pathlib import Path
import secrets
import argparse
import shutil
from typing import Union, Sequence
import os
import sys

# ==============================
# Constants
# ==============================

REPO_ROOT = Path(__file__).resolve().parents[2]

BACKEND_PROJECTS_DIR = REPO_ROOT / "backend" / "projects"
FRONTEND_PROJECTS_DIR = REPO_ROOT / "frontend" / "proyectos"
LIQUIBASE_ROOT = Path("docker") / "liquibase"
LIQUIBASE_PROJECTS_DIR = LIQUIBASE_ROOT / "changelog" / "projects"

BASE_REQUIREMENTS = REPO_ROOT / "backend" / "requirements.txt"

# ==============================
# Helpers
# ==============================

def run(cmd: Union[str, Sequence[str]], cwd=None, env=None, input_text=None, **kwargs):
    """
    Ejecuta un comando del sistema mostrando stdout/stderr.
    Falla inmediatamente si el comando devuelve error.

    - Si cmd es str → se ejecuta vía shell
    - Si cmd es lista → ejecución directa (recomendado)
    """
    print("→", cmd if isinstance(cmd, str) else " ".join(cmd))

    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        shell=isinstance(cmd, str),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = process.communicate(input=input_text)

    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    if process.returncode != 0:
        raise RuntimeError(f"❌ Comando falló ({process.returncode})")

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--project", required=True)

    parser.add_argument("--backend", action="store_true")
    parser.add_argument("--frontend", action="store_true")

    # Backend
    parser.add_argument("--backend-port", type=int, default=8000)

    # Frontend
    parser.add_argument("--frontend-port", type=int, default=3000)

    # Database
    parser.add_argument("--db-host", required=True)
    parser.add_argument("--db-port", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--db-user", required=True)
    parser.add_argument("--db-password", required=True)

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


def create_virtualenv(project_dir: Path):
    """
    Crea el entorno virtual usando Python 3.14 explícitamente.
    Falla si Python 3.14 no está disponible.
    """
    python_exe = "py"

    run(
        [python_exe, "-3.14", "-m", "venv", ".venv"],
        cwd=project_dir,
        check=True,
    )

def install_dependencies(project_dir: Path):
    """
    Copia el requirements.txt base al proyecto e instala dependencias
    usando el Python del virtualenv.
    """
    python_exe = project_dir / ".venv" / "Scripts" / "python.exe"

    base_requirements = REPO_ROOT / "backend" / "requirements.txt"
    target_requirements = project_dir / "requirements.txt"

    if not base_requirements.exists():
        raise FileNotFoundError(
            f"No se encontró el requirements base en {base_requirements}"
        )

    # Copiar requirements.txt al proyecto (sobrescribe si existe)
    shutil.copy(base_requirements, target_requirements)

    # Instalar dependencias
    run(
        [
            str(python_exe),
            "-m",
            "pip",
            "install",
            "-r",
            "requirements.txt",
        ],
        cwd=project_dir,
        check=True,
    )

# ==============================
# Django
# ==============================

def create_django_project(project_name: str, project_dir: Path):
    """
    Inicializa el proyecto Django usando el Python del venv.
    """
    python_exe = project_dir / ".venv" / "Scripts" / "python.exe"

    run(
        [
            str(python_exe),
            "-m",
            "django",
            "startproject",
            project_name,
            ".",
        ],
        cwd=project_dir,
        check=True,
    )


# ==============================
# Settings
# ==============================

def configure_settings(project_name, project_dir):
    """
    Writes a runtime-driven Django settings.py.

    Infrastructure is NOT defined here.
    All configuration is provided at runtime via .env (orc-controlled).
    """

    settings_path = project_dir / project_name / "settings.py"

    settings = f'''"""
Django settings for {project_name} project.

Runtime-driven configuration.
This project does not define infrastructure.
"""

from pathlib import Path
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

BACKEND_DIR = Path(
    os.environ.get("BACKEND_DIR", BASE_DIR)
).resolve()

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

APPS_DIR = BACKEND_DIR / "apps"

ENV_PATH = BASE_DIR / ".env"

for p in (BACKEND_DIR, APPS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    raise ImproperlyConfigured(f".env file not found at {{ENV_PATH}}")

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ImproperlyConfigured(f"Missing environment variable: {{name}}")
    return value


# -------------------------------------------------------------------
# Core settings
# -------------------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG").lower() == "true"
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(",")


# -------------------------------------------------------------------
# Application definition
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "corsheaders",
    "apps.base",
    "apps.auditoria",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{project_name}.urls"

TEMPLATES = [
    {{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {{
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }},
    }},
]

WSGI_APPLICATION = "{project_name}.wsgi.application"


# -------------------------------------------------------------------
# Database (runtime-controlled)
# -------------------------------------------------------------------

DATABASES = {{
    "default": {{
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }}
}}


# -------------------------------------------------------------------
# Authentication
# -------------------------------------------------------------------

AUTH_USER_MODEL = "base.User"

AUTH_PASSWORD_VALIDATORS = [
    {{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}},
]


# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -------------------------------------------------------------------
# Static files
# -------------------------------------------------------------------

STATIC_URL = "static/"


# -------------------------------------------------------------------
# CORS / CSRF (runtime-controlled)
# -------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
CORS_ALLOW_CREDENTIALS = True
'''

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

def create_postgres_schema(args):
    """
    Crea un schema PostgreSQL si no existe.
    """
    schema_name = args.project
    try:
        import psycopg2  # type: ignore

        conn = psycopg2.connect(
            dbname="postgres",
            user=args.db_user,
            password=args.db_password,
            host=args.db_host,
            port=args.db_port,
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

    if any(project_dir.iterdir()):
        raise RuntimeError("El directorio frontend no está vacío")

    env = os.environ.copy()
    env["CI"] = "true"

    run(
    ["npx.cmd", "create-vite", ".", "--template", "react"],
    cwd=project_dir, env=env,
    )
    run(["npm.cmd", "install"], cwd=project_dir, env=env)

    patch_vite_config(project_dir)

    return project_dir

def patch_vite_config(project_dir):
    vite_config = project_dir / "vite.config.js"

    if not vite_config.exists():
        raise FileNotFoundError(
            f"No se encontró vite.config.js en {project_dir}"
        )

    content = vite_config.read_text(encoding="utf-8")

    if "server:" in content:
        # Ya fue modificado antes
        return

    patched = content.replace(
        "export default defineConfig({",
        "export default defineConfig({\n  server: {\n    port: 3000,\n  },"
    )

    vite_config.write_text(patched, encoding="utf-8")

# ==============================
# Main
# ==============================

def main():
    args = parse_args()

    if args.project:
        project_name = args.project
    else:
        project_name = ask_project_name()
    if not args.backend and not args.frontend:
        args.backend = True
        args.frontend = True

    project_dir = create_project_directory(project_name)

    print(f"\n🚀 Creando proyecto '{project_name}'\n")

    if args.backend:
        create_virtualenv(project_dir)
        install_dependencies(project_dir)
        create_django_project(args.project, project_dir)
        configure_settings(args.project, project_dir)
        configure_vscode(project_dir)
        create_postgres_schema(args)
        register_project_in_liquibase(args.project)

    if args.frontend:
        create_frontend_project(args.project)

    print("\n🎉 Proyecto creado correctamente")
    print("📌 El schema será gestionado por Liquibase")
    print(f"cd backend/{project_name}")
    print("python manage.py runserver")


if __name__ == "__main__":
    main()
