from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.scripts.generators.paths import APPS_DIR

CONTROLLER_TEMPLATE = """from django.db.models import Q
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.{app_name}.models.{model_name} import {ModelName}
from apps.{app_name}.serializers.{model_name}_serializer import (
    {ModelName}CreateSerializer,
    {ModelName}UpdateSerializer,
    {ModelName}RetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class Permisos{ModelName}(PermisoGroup):
    VIEW=Constant("{app_name}.{model_name}.view")
    CREATE=Constant("{app_name}.{model_name}.create")
    UPDATE=Constant("{app_name}.{model_name}.update")
    DESTROY=Constant("{app_name}.{model_name}.destroy")


class {ModelName}RestController(ModelRestController):
    label = "{ModelName}"
    model = {ModelName}
    url = "{model_name_kebab}"
    create_serializer = {ModelName}CreateSerializer
    update_serializer = {ModelName}UpdateSerializer
    retrieve_serializer = {ModelName}RetrieveSerializer    
    permisos = Permisos{ModelName}
"""

OPTIONS_VIEW_TEMPLATE='''
from framework.api.options import BaseOptionsAPIView
from apps.{app_name}.models.{model_name} import {ModelName}

class {ModelName}OptionsView(BaseOptionsAPIView):
    model = {ModelName}
    url='{model_name_kebab}'
    desc_field='Descripcion'
    permisos=[]

'''
def generate_rest_controller(definition: DomainModelDefinition) -> None:
    """
    Genera el RestController correspondiente a un modelo de dominio.
    - ConstantModel → OptionsView
    - Modelo normal → RestController estándar
    """
    file_path = resolve_rest_controller_path(definition)
    content = render_rest_controller_content(definition)

    write_file(file_path, content)

    print(f"✔ RestController generado: {file_path}")

def resolve_rest_controller_path(definition: DomainModelDefinition):
    return (
        APPS_DIR
        / definition.app_name
        / "rest_controllers"
        / f"{definition.model_name}_rest_controller.py"
    )

def render_rest_controller_content(definition: DomainModelDefinition) -> str:
    """
    Devuelve el contenido del controller según el tipo de modelo.
    """
    if definition.is_constant_model:
        return render_options_view(definition)

    return render_standard_rest_controller(definition)

def render_options_view(definition: DomainModelDefinition) -> str:
    """
    Renderiza un OptionsView para ConstantModels.
    """
    return OPTIONS_VIEW_TEMPLATE.format(
        model_name=definition.model_name,
        ModelName=definition.ModelName,
        app_name=definition.app_name,
        model_name_kebab=to_kebab_case(definition.model_name),
    )

def render_standard_rest_controller(definition: DomainModelDefinition) -> str:
    """
    Renderiza un RestController estándar.
    """
    return CONTROLLER_TEMPLATE.format(
        model_name=definition.model_name,
        ModelName=definition.ModelName,
        app_name=definition.app_name,
        model_name_kebab=to_kebab_case(definition.model_name),
    )

def to_kebab_case(value: str) -> str:
    return value.replace("_", "-")

def write_file(path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
