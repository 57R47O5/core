import os
import sys
from pathlib import Path
import pytest

# backend/apps/conftest.py

# ─────────────────────────────────────────────────────────────
# Resolución de paths reales
# ─────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend" 
# .../backend

PROJECT_ROOT = BACKEND_ROOT / "projects" / "prueba"
# .../backend/projects/prueba

# Orden IMPORTA:
# 1. backend → para `import apps.xxx`
# 2. project → para `import config.xxx`
sys.path.insert(0, str(BACKEND_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))


# ─────────────────────────────────────────────────────────────
# Django setup
# ─────────────────────────────────────────────────────────────

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.base",
)

import django
django.setup()

# ─────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient(HTTP_USER_AGENT="Mozilla/5.0")


@pytest.fixture
def auth_client(client):
    response = client.post(
        "/login/",
        {"identifier": "esteban", "password": "142857"},
        format="json",
    )

    if response.status_code != 200:
        pytest.fail(
            f"""
            ❌ Falló autenticación en fixture auth_client

            Status: {response.status_code}
            Body: {response.content.decode()}
            """
        )

    token = response.json().get("token")
    if not token:
        pytest.fail("Login OK pero no devolvió token")

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client
