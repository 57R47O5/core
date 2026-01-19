import os
from orchestrator.scripts.generators.paths import APPS_DIR
from orchestrator.utils.naming import to_snake_case, to_pascal_case


def generate_urls(app_name:str, model_name:str):
    """
    Genera un urls.py básico usando SimpleRouter.
    Basado directamente en el template proporcionado por el usuario.
    """

    # Ej.: modelo Paciente → paciente
    model_snake = to_snake_case(model_name)
    ModelName = to_pascal_case(model_snake)
    model_kebab = model_snake.replace("_", "-")

    # Controller
    controller_name = f"{ModelName}RestController"

    file_path = APPS_DIR / app_name / "urls" / f"{model_snake}_urls.py"

    # Template base proporcionado por el usuario
    content = f"""
from django.urls import path
from rest_framework import routers
from apps.{app_name}.rest_controllers.{model_snake}_rest_controller import (
    {controller_name}
)

router = routers.SimpleRouter()
router.register(r'{model_kebab}', {controller_name}, '{model_kebab}')

urlpatterns = []

urlpatterns += router.urls
"""

    # Escribimos SIEMPRE el archivo completo (lo sobreescribimos por ahora)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"📝 Archivo URLs generado: {file_path}")
