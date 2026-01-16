from pathlib import Path

REPO_ROOT = Path(r"C:/Users/Seraf/proyectos")   # hardcode explícito
BACKEND_DIR = REPO_ROOT / "backend"
APPS_DIR = BACKEND_DIR / "apps"

BASE_APP_MODELS_DIR = APPS_DIR / "base" / "models"
LIQUIBASE_CHANGELOG_APPS = REPO_ROOT / "liquibase" / "changelog" / "apps"