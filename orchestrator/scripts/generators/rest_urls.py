from orchestrator.scripts.generators.paths import APPS_DIR
from orchestrator.utils.naming import to_pascal_case

def generate_rest_urls(app_name: str):
    """
    Genera apps/<app>/rest_urls.py registrando automáticamente
    todos los RestControllers encontrados en rest_controllers/.
    """

    app_dir = APPS_DIR / app_name
    controllers_dir = app_dir / "rest_controllers"
    output_file = app_dir / "rest_urls.py"

    if not controllers_dir.exists():
        print(f"[GEN][urls] No existe {controllers_dir}, nada que hacer")
        return True

    imports = []
    registrations = []

    for file in sorted(controllers_dir.iterdir()):
        if not file.name.endswith("_rest_controller.py"):
            continue

        # user_rol_rest_controller.py → user_rol
        model_snake = file.name.replace("_rest_controller.py", "")
        ModelName = to_pascal_case(model_snake)
        controller_name = f"{ModelName}RestController"
        model_kebab = model_snake.replace("_", "-")

        if model_snake != "base":
            imports.append(
                f"from apps.{app_name}.rest_controllers.{model_snake}_rest_controller "
                f"import {controller_name}"
            )

            registrations.append(
                f"router.register(r'{model_kebab}', {controller_name}, '{model_kebab}')"
            )

    if not imports:
        print(f"[GEN][urls] No se encontraron rest controllers en {controllers_dir}")
        return True

    content = f'''\
from rest_framework import routers

router = routers.SimpleRouter()

{chr(10).join(imports)}

{chr(10).join(registrations)}

urlpatterns = router.urls
'''

    output_file.write_text(content, encoding="utf-8")

    print(f"[GEN][urls] rest_urls.py generado: {output_file}")
    return True
