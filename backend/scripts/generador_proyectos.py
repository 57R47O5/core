import os
import subprocess
import shutil
from pathlib import Path
import sys


def run(cmd, cwd=None):
    print(f"→ Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    if len(sys.argv) < 2:
        print("Uso: python generador_proyectos.py <nombre_proyecto>")
        sys.exit(1)

    nombre = sys.argv[1]

    backend_dir = Path(__file__).resolve().parents[1]
    proyectos_dir = backend_dir / "proyectos"
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
    fixtures_dir = proyecto_dir / "roles" / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)

    (fixtures_dir / "roles.json").write_text("[]", encoding="utf8")

    # 7. Registrar apps en settings.py
    settings_path = proyecto_dir / nombre / "settings.py"
    settings_text = settings_path.read_text(encoding="utf8")

    new_settings = settings_text.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n"
        "    'apps.base',\n"
        "    'roles',"
    )

    settings_path.write_text(new_settings, encoding="utf8")

    # 8. Agregar path a apps en settings
    with open(settings_path, "a", encoding="utf8") as f:
        f.write("\nimport sys\n")
        f.write("from pathlib import Path\n")
        f.write("BASE_DIR = Path(__file__).resolve().parent.parent\n")
        f.write("sys.path.append(str(BASE_DIR / '..' / 'apps'))\n")

    # 9. Migraciones
    run(["uv", "run", "python", "manage.py", "makemigrations"], cwd=proyecto_dir)
    run(["uv", "run", "python", "manage.py", "migrate"], cwd=proyecto_dir)

    print("\n🎉 Proyecto creado exitosamente")
    print(f"📁 Ubicación: backend/proyectos/{nombre}")
    print("▶ Para iniciar el servidor:")
    print(f"cd backend/proyectos/{nombre}")
    print("uv run python manage.py runserver")


if __name__ == "__main__":
    main()
