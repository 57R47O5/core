import os
import subprocess
import shutil
from pathlib import Path
import sys


def run(cmd, cwd=None):
    print(f"→ Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

import secrets

def create_env_file(path, nombre_db):
    env_path = path / ".env"

    print(f"📝 Creando archivo .env en: {env_path}")

    secret_key = secrets.token_urlsafe(50)

    content = f"""
# ==========================================
# CONFIGURACIÓN GENERAL DJANGO
# ==========================================
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ==========================================
# BASE DE DATOS POSTGRESQL
# ==========================================
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB={nombre_db}
POSTGRES_USER=postgres
POSTGRES_PASSWORD=142857
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

# ==========================================
# CORS / CSRF
# ==========================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=True
"""

    env_path.write_text(content.strip() + "\n", encoding="utf8")

    print("✅ Archivo .env creado correctamente")


def create_postgres_db(nombre_db, user="postgres", password="142857", host="localhost", port="5433"):
    print(f"🏗️ Creando base de datos PostgreSQL: {nombre_db}")

    try:
        import psycopg2
        conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {nombre_db};")
        cur.close()
        conn.close()
        print(f"✅ Base de datos {nombre_db} creada")
    except Exception as e:
        print(f"⚠️ No se pudo crear la base de datos (quizás ya existe): {e}")



def main():
    if len(sys.argv) < 2:
        print("Uso: python generador_proyectos.py <nombre_proyecto>")
        sys.exit(1)

    nombre = sys.argv[1]

    backend_dir = Path(__file__).resolve().parents[1]
    proyectos_dir = backend_dir 
    proyectos_dir.mkdir(exist_ok=True)

    proyecto_dir = proyectos_dir / nombre
    proyecto_dir.mkdir(exist_ok=True)

    print(f"🚀 Creando proyecto Django: {nombre}")

    # 1. Crear entorno virtual
    run(["uv", "venv", ".venv"], cwd=proyecto_dir)

    # 2. Instalar dependencias base del backend
    req = backend_dir / "requirements.txt"
    if req.exists():
        run(["uv", "pip", "install", "-r", str(req)], cwd=proyecto_dir)
    else:
        print("⚠️ No se encontró requirements.txt en backend/. Instalando solo Django")
        run(["uv", "pip", "install", "django"], cwd=proyecto_dir)

    # 3. Crear proyecto Django
    run(["uv", "run", "django-admin", "startproject", nombre, "."], cwd=proyecto_dir)

    # 4. Crear app local "roles"
    run(["uv", "run", "python", "manage.py", "startapp", "roles"], cwd=proyecto_dir)

    # 5. Generar modelos roles (plantilla mínima)
    roles_models = proyecto_dir / "roles" / "models.py"
    roles_models.write_text(
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

    # 6. Crear carpeta de fixtures
    fixtures_dir = proyecto_dir / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)

    (fixtures_dir / "roles.json").write_text("[]", encoding="utf8")

    # 7. Registrar apps en settings.py
    settings_path = proyecto_dir / nombre / "settings.py"
    settings_text = settings_path.read_text(encoding="utf8")

    new_settings = settings_text.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n"
        "    'base.apps.BaseConfig',\n"
        "    'auditoria.apps.AuditoriaConfig',\n"
        "    'roles',\n"
    )

    settings_path.write_text(new_settings, encoding="utf8")

    # 8. Agregar path a apps en settings
    with open(settings_path, "a", encoding="utf8") as f:
        f.write("\nimport sys\n")
        f.write("from pathlib import Path\n")
        f.write("BASE_DIR = Path(__file__).resolve().parent.parent\n")
        f.write("sys.path.append(str(BASE_DIR / '..' / 'apps'))\n")

    # Creacion de db

    create_postgres_db(nombre)

    # 10. Configurar DATABASES basado en variables de entorno
    with open(settings_path, "a", encoding="utf8") as f:
        f.write("\n\n# ==============================\n")
        f.write("# CONFIGURACIÓN BASE DE DATOS\n")
        f.write("# ==============================\n")
        f.write("import os\n")
        f.write("DATABASES = {\n")
        f.write("    'default': {\n")
        f.write("        'ENGINE': os.getenv('DB_ENGINE', ''),\n")
        f.write(f"        'NAME': os.getenv('POSTGRES_DB', ''),\n")
        f.write("        'USER': os.getenv('POSTGRES_USER', ''),\n")
        f.write("        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),\n")
        f.write("        'HOST': os.getenv('POSTGRES_HOST', ''),\n")
        f.write("        'PORT': os.getenv('POSTGRES_PORT', ''),\n")
        f.write("    }\n")
        f.write("}\n")

    # 11. Agregar configuración de CORS
    with open(settings_path, "a", encoding="utf8") as f:
        f.write("\n\n# ==============================\n")
        f.write("# CONFIGURACIÓN CORS\n")
        f.write("# ==============================\n")
        f.write("CORS_ALLOWED_ORIGINS = [\n")
        f.write("os.getenv('CORS_ALLOWED_ORIGINS', ''),")
        f.write("]\n")
        f.write("CORS_ALLOW_CREDENTIALS = True\n")
        f.write("CORS_ALLOW_METHODS = ['GET','POST','OPTIONS','PUT','PATCH','DELETE']\n")
        f.write("CSRF_TRUSTED_ORIGINS = [\n")
        f.write("os.getenv('CORS_ALLOWED_ORIGINS', ''),")
        f.write("]\n")

    settings_text = settings_path.read_text(encoding="utf8")
    settings_text = settings_text.replace(
        "MIDDLEWARE = [",
        "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',"
    )

    settings_path.write_text(settings_text, encoding="utf8")

    # 9. Migraciones
    run(["uv", "run", "python", "manage.py", "makemigrations"], cwd=proyecto_dir)
    run(["uv", "run", "python", "manage.py", "migrate"], cwd=proyecto_dir)

    print("\n🎉 Proyecto creado exitosamente")
    print(f"📁 Ubicación: backend/{nombre}")
    print("▶ Para iniciar el servidor:")
    print(f"cd backend/{nombre}")
    print("uv run python manage.py runserver")


if __name__ == "__main__":
    main()
