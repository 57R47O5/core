"""
Setup inicial del monorepo.

Responsabilidad:
- Preparar infraestructura compartida
- Integrar Liquibase, Docker y GitLab
- No crear proyectos ni lógica Django

Idempotente y reversible.
"""

from pathlib import Path
import subprocess
import sys


# ==============================
# Helpers
# ==============================

def run(cmd, cwd=None):
    """
    Ejecuta un comando del sistema.
    """
    print("→", " ".join(map(str, cmd)))
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_dir(path: Path):
    """
    Crea un directorio si no existe.
    """
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str):
    """
    Escribe un archivo solo si no existe.
    """
    if path.exists():
        print(f"✔ Archivo existente: {path}")
        return
    path.write_text(content, encoding="utf8")
    print(f"✔ Archivo creado: {path}")


# ==============================
# Liquibase
# ==============================

def setup_liquibase(root: Path):
    """
    Prepara estructura base de Liquibase.
    """
    liquibase_dir = root / "liquibase"
    changelog_dir = liquibase_dir / "changelog"

    ensure_dir(changelog_dir)

    write_file(
        liquibase_dir / "liquibase.properties",
        """changeLogFile=changelog/db.changelog-master.yaml
url=jdbc:postgresql://localhost:5433/postgres
username=postgres
password=142857
driver=org.postgresql.Driver
"""
    )

    write_file(
        changelog_dir / "db.changelog-master.yaml",
        """databaseChangeLog:
  - includeAll:
      path: changelog/
"""
    )


# ==============================
# Docker
# ==============================

def setup_docker(root: Path):
    """
    Prepara archivos Docker base.
    """
    docker_dir = root / "docker"
    ensure_dir(docker_dir)

    write_file(
        docker_dir / "Dockerfile.backend",
        """FROM python:3.14-slim

WORKDIR /app

COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app

CMD ["bash"]
"""
    )

    write_file(
        docker_dir / "docker-compose.yml",
        """version: "3.9"

services:
  postgres:
    image: postgres:16
    ports:
      - "5433:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 142857
      POSTGRES_DB: postgres
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
"""
    )


# ==============================
# GitLab CI
# ==============================

def setup_gitlab_ci(root: Path):
    """
    Crea pipeline base para GitLab CI.
    """
    write_file(
        root / ".gitlab-ci.yml",
        """stages:
  - test

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

test:
  stage: test
  image: python:3.14
  before_script:
    - pip install uv
  script:
    - uv pip install -r backend/requirements.txt
    - echo "Pipeline base OK"
"""
    )


# ==============================
# Validaciones
# ==============================

def validate_structure(root: Path):
    """
    Valida que estamos en el root correcto del monorepo.
    """
    required = ["backend", "backend/apps", "backend/scripts"]
    for rel in required:
        if not (root / rel).exists():
            print(f"❌ Estructura inválida, falta: {rel}")
            sys.exit(1)


# ==============================
# Main
# ==============================

def main():
    print("\n=== Setup inicial del monorepo ===\n")

    root = Path(__file__).resolve().parents[2]
    validate_structure(root)

    setup_liquibase(root)
    setup_docker(root)
    setup_gitlab_ci(root)

    print("\n✅ Monorepo inicializado correctamente")
    print("Siguiente paso: crear proyectos con el generador")


if __name__ == "__main__":
    main()
