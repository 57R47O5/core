from orchestrator.scripts.generators.paths import BACKEND_DIR
from orchestrator.scripts.utils.naming import to_snake_case, to_pascal_case

MODELS_ROOT = BACKEND_DIR / "apps"

_MODEL_REGISTRY: dict[str, str] | None = None

def build_model_registry() -> dict[str, str]:
    """
    Retorna:
        {
            "Paciente": "pacientes",
            "Doctor": "consultorio",
            "User": "auth",
        }
    """
    registry: dict[str, str] = {}

    for app_dir in MODELS_ROOT.iterdir():
        if not app_dir.is_dir():
            continue

        models_dir = app_dir / "models"
        if not models_dir.exists():
            continue

        app_name = app_dir.name

        for model_file in models_dir.glob("*.py"):
            if model_file.name == "__init__.py":
                continue

            model_name = model_file.stem  # paciente.py
            ModelName = to_pascal_case(model_name)

            if ModelName in registry:
                raise RuntimeError(
                    f"Modelo '{ModelName}' definido en más de una app: "
                    f"{registry[ModelName]} y {app_name}"
                )

            registry[ModelName] = app_name

    return registry

def get_model_registry() -> dict[str, str]:
    global _MODEL_REGISTRY

    if _MODEL_REGISTRY is None:
        _MODEL_REGISTRY = build_model_registry()

    return _MODEL_REGISTRY

def resolve_model_app(ModelName: str) -> str:
    """
    Dado un modelo en PascalCase, retorna la app donde está definido.
    """
    registry = get_model_registry()

    try:
        return registry[ModelName]
    except KeyError:
        raise RuntimeError(
            f"No se pudo resolver la app del modelo '{to_snake_case(ModelName)}'. "
            f"Modelos conocidos: {sorted(registry.keys())}"
        )
