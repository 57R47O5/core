from scripts.generators.paths import APPS_DIR
from scripts.generators.domain_model_definition import DomainModelDefinition

def generate_urls(definition:DomainModelDefinition):
    """
    Genera un urls.py básico usando SimpleRouter.
    Basado directamente en el template proporcionado por el usuario.
    """

    # Ej.: modelo Paciente → paciente
    model_name = definition.model_name
    ModelName = definition.ModelName
    app_name = definition.app_name
    model_kebab = model_name.replace("_", "-")

    # Controller
    controller_name = f"{ModelName}RestController"

    file_path = APPS_DIR / app_name / "urls" / f"{model_name}_urls.py"

    # Template base proporcionado por el usuario
    content = f"""
from rest_framework import routers
from apps.{app_name}.rest_controllers.{model_name}_rest_controller import (
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
