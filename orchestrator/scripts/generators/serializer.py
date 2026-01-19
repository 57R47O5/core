from orchestrator.scripts.generators.paths import APPS_DIR
from orchestrator.utils.naming import to_snake_case, to_pascal_case

SERIALIZER_TEMPLATE = """from rest_framework import serializers
from apps.{app_name}.models.{model_snake} import {ModelName}


class {ModelName}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {ModelName}
        fields = "__all__"


class {ModelName}CreateSerializer({ModelName}Serializer):
    pass


class {ModelName}UpdateSerializer({ModelName}Serializer):
    pass


class {ModelName}RetrieveSerializer({ModelName}Serializer):
    pass
"""


def generate_serializer(app_name: str, model_name: str):
    """
    Genera un serializer base para el modelo dado.
    - ModelName = PascalCase → "Paciente"
    - model_name = lowercase → "paciente"
    - model_snake = snake_case → "paciente"
    """

    model_snake = to_snake_case(model_name)
    ModelName = to_pascal_case(model_snake)

    file_path = APPS_DIR / app_name / "serializers" / f"{model_snake}_serializer.py"

    content = SERIALIZER_TEMPLATE.format(
        ModelName=ModelName,
        model_name=model_name,
        model_snake=model_snake,
        app_name=app_name,
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✔ Serializer generado: {file_path}")
