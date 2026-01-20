from orchestrator.scripts.generators.paths import APPS_DIR
from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.utils.naming import to_snake_case


def generate_serializer(definition: DomainModelDefinition):
    """
    Genera serializers DRF basados en la DomainModelDefinition.

    Reglas:
    - FK embebida → serializer anidado completo
    - FK no embebida → {id, controller, nombre}
    - CreateSerializer con save atómico para embebidos
    """

    model_name = definition.model_name          # snake_case
    ModelName = definition.ModelName             # PascalCase
    app_name = definition.app_name

    file_path = (
        APPS_DIR / app_name / "serializers" / f"{model_name}_serializer.py"
    )

    imports = [
        "from rest_framework import serializers",
        f"from apps.{app_name}.models.{model_name} import {ModelName}",
    ]

    serializer_fields = []
    serializer_field_names = ['"id"']

    link_serializers = []
    embedded_creates = []

    # --------------------------------------------------
    # Procesamiento de campos
    # --------------------------------------------------
    for field in definition.extra_fields:
        serializer_field_names.append(f'"{field.name}"')

        if not field.is_foreign_key:
            continue

        ref_model = field.references_model
        ref_app = field.references_app
        ref_snake = to_snake_case(ref_model)
        controller_name = ref_snake.replace("_", "-")

        # ----------------------------
        # FK EMBEBIDA
        # ----------------------------
        if field.is_embedded:
            imports.append(
                f"from apps.{ref_app}.serializers.{ref_snake}_serializer "
                f"import {ref_model}Serializer"
            )

            serializer_fields.append(
                f"    {field.name} = {ref_model}Serializer()"
            )

            embedded_creates.append(field)

        # ----------------------------
        # FK NO EMBEBIDA
        # ----------------------------
        else:
            link_serializer_name = f"{ref_model}LinkSerializer"

            if link_serializer_name not in link_serializers:
                imports.append(
                    f"from apps.{ref_app}.models.{ref_snake} import {ref_model}"
                )

                link_serializers.append(
                    f"""
class {link_serializer_name}(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = {ref_model}
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "{controller_name}"
""".rstrip()
                )

            serializer_fields.append(
                f"    {field.name} = {link_serializer_name}()"
            )

    # --------------------------------------------------
    # CreateSerializer.create() atómico
    # --------------------------------------------------
    create_method = ""

    if embedded_creates:
        create_method = """
    def create(self, validated_data):
        from django.db import transaction

        with transaction.atomic():
"""

        for field in embedded_creates:
            create_method += f"""
            {field.name}_data = validated_data.pop("{field.name}")
            {field.name}_obj = self.fields["{field.name}"].create({field.name}_data)
            validated_data["{field.name}"] = {field.name}_obj
"""

        create_method += f"""
            return {ModelName}.objects.create(**validated_data)
"""

    # --------------------------------------------------
    # Construcción final del archivo
    # --------------------------------------------------
    content = "\n".join(imports) + "\n\n"

    if link_serializers:
        content += "\n\n".join(link_serializers) + "\n\n"

    content += f"""
class {ModelName}Serializer(serializers.ModelSerializer):
{chr(10).join(serializer_fields) if serializer_fields else "    pass"}

    class Meta:
        model = {ModelName}
        fields = [
            {", ".join(serializer_field_names)}
        ]


class {ModelName}CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = {ModelName}
        fields = "__all__"
{create_method if create_method else "    pass"}


class {ModelName}UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = {ModelName}
        fields = "__all__"


class {ModelName}RetrieveSerializer({ModelName}Serializer):
    pass
""".lstrip()

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✔ Serializer generado: {file_path}")
