import subprocess
from pathlib import Path
import secrets
import os


# ==============================
# Helpers
# ==============================

def run(cmd, cwd=None, env=None):
    print("→", " ".join(map(str, cmd)))
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


# ==============================
# Utilidades
# ==============================

def create_env_file(path, nombre_db):
    secret_key = secrets.token_urlsafe(50)

    (path / ".env").write_text(
        f"""# DJANGO
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# DATABASE
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB={nombre_db}
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


def create_postgres_db(nombre_db):
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="142857",
            host="localhost",
            port="5433",
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {nombre_db};")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ DB posiblemente existente: {e}")


# ==============================
# Main
# ==============================

def main():
    nombre = input("👉 Nombre del proyecto: ").strip()

    backend_dir = Path(__file__).resolve().parents[1]
    proyecto_dir = backend_dir / nombre
    proyecto_dir.mkdir(exist_ok=True)

    print(f"\n🚀 Creando proyecto Django '{nombre}' (monorepo + uv)\n")

    # 1. Venv
    run(["uv", "venv", ".venv"], cwd=proyecto_dir)

    # 2. Dependencias
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
        cwd=proyecto_dir,
    )

    # 3. Proyecto Django
    run(
        ["uv", "run", "django-admin", "startproject", nombre, "."],
        cwd=proyecto_dir,
    )

    # 4. App roles
    run(
        ["uv", "run", "python", "manage.py", "startapp", "roles"],
        cwd=proyecto_dir,
    )

    # 5. Models roles
    (proyecto_dir / "roles" / "models.py").write_text(
        """from django.db import models
from apps.base.models import User


class Role(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')
""",
        encoding="utf8",
    )

    # 6. Settings
    settings_path = proyecto_dir / nombre / "settings.py"
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
        "    'apps.auditoria',\n"
        "    'roles',",
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
    # VS Code config (.vscode)
    # ==============================

    vscode_dir = proyecto_dir / ".vscode"
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


    # 7. Env + DB
    create_env_file(proyecto_dir, nombre)
    create_postgres_db(nombre)

    # 8. Migraciones
    run(["uv", "run", "python", "manage.py", "makemigrations"], cwd=proyecto_dir)
    run(["uv", "run", "python", "manage.py", "migrate"], cwd=proyecto_dir)

    print("\n🎉 Proyecto creado correctamente")
    print(f"cd backend/{nombre}")
    print("uv run python manage.py runserver")


if __name__ == "__main__":
    main()
