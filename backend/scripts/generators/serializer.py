# generators/serializer.py

import os

SERIALIZER_TEMPLATE = """from rest_framework import serializers
from apps.{app_name}.models.{model_name} import {ModelName}


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


def generate_serializer(ModelName: str, model_name: str, model_snake: str, app_name: str = "carteles"):
    """
    Genera un serializer base para el modelo dado.
    - ModelName = PascalCase → "Paciente"
    - model_name = lowercase → "paciente"
    - model_snake = snake_case → "paciente"
    """
    directory = f"output/{model_name}"
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f"{model_snake}_serializer.py")

    content = SERIALIZER_TEMPLATE.format(
        ModelName=ModelName,
        model_name=model_name,
        model_snake=model_snake,
        app_name=app_name,
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✔ Serializer generado: {file_path}")
