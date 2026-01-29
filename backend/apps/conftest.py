import os
import sys
from pathlib import Path
import pytest
from django.db import connection, transaction

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

@pytest.fixture(scope="session")
def django_db_setup():
    # pytest-django NO crea ni destruye la DB
    pass

@pytest.fixture(autouse=True)
def enable_db_access_for_tests(django_db_blocker):
    with django_db_blocker.unblock():
        with transaction.atomic():
            yield
            # rollback automático

class UsuarioPrueba():
    nombre="usuario_prueba"
    password="password"

@pytest.fixture
def user(db):
    from apps.auth.models.user import User
    from framework.security.passwords import hash_password
    return User.objects.create(
        username=UsuarioPrueba.nombre,
        password_hash=hash_password(UsuarioPrueba.password),
    )

@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient(HTTP_USER_AGENT="Mozilla/5.0")


@pytest.fixture
def auth_client(client, user):
    response = client.post(
        "/login/",
        {
            "identifier": UsuarioPrueba.nombre, 
            "password": UsuarioPrueba.password},
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
