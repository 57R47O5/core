from scripts.generators.paths import BACKEND_DIR

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
            ModelName = model_name.capitalize()  # Paciente

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

def resolve_model_app(model_name: str) -> str:
    """
    Dado un modelo en PascalCase, retorna la app donde está definido.
    """
    registry = get_model_registry()

    try:
        return registry[model_name]
    except KeyError:
        raise RuntimeError(
            f"No se pudo resolver la app del modelo '{model_name}'. "
            f"Modelos conocidos: {sorted(registry.keys())}"
        )
