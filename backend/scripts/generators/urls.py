import os


def generate_urls(app_name, model_name):
    """
    Genera un urls.py básico usando SimpleRouter.
    Basado directamente en el template proporcionado por el usuario.
    """

    # Ej.: modelo Paciente → paciente
    model_snake = model_name.lower()
    model_kebab = model_snake.replace("_", "-")

    # Controller
    controller_name = f"{model_name}RestController"

    folder = f"apps/{app_name}"
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, "urls.py")

    # Template base proporcionado por el usuario
    content = f"""
from django.urls import path
from rest_framework import routers
from apps.{app_name}.views.{model_snake}_view import (
    {controller_name}
)

router = routers.SimpleRouter()
router.register(r'{model_kebab}', {controller_name}, '{model_kebab}')

urlpatterns = []

urlpatterns += router.urls
"""

    # Escribimos SIEMPRE el archivo completo (lo sobreescribimos por ahora)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

    print(f"📝 Archivo URLs generado: {path}")
