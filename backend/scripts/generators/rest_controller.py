import os
from datetime import datetime


CONTROLLER_TEMPLATE = """from django.db.models import Q
from datetime import datetime

from base.framework.api.options import BaseOptionsAPIView
from apps.{app_name}.models.{model_name} import {ModelName}
from apps.{app_name}.serializers.{model_name}_serializer import (
    {ModelName}CreateSerializer,
    {ModelName}UpdateSerializer,
    {ModelName}RetrieveSerializer,
from controllers.base.base_rest_controller import ModelRestController


class {ModelName}RestController(ModelRestController):
    model = {ModelName}
    create_serializer = {ModelName}CreateSerializer
    update_serializer = {ModelName}UpdateSerializer
    retrieve_serializer = {ModelName}RetrieveSerializer

    def _get_filter(self, params):
        filtros = Q()

        # --- filtros automáticos por coincidencia de campos ---
        for campo, valor in params.items():
            if valor:
                filtros &= Q(**{{
                    f"{{campo}}__icontains": valor.strip()
                }})

        # --- filtros especiales (fecha_desde / fecha_hasta) ---
        fecha_desde = params.get("fecha_desde")
        fecha_hasta = params.get("fecha_hasta")

        if fecha_desde:
            try:
                fecha = datetime.fromisoformat(fecha_desde)
                filtros &= Q(fecha_creacion__date__gte=fecha.date())
            except:
                pass

        if fecha_hasta:
            try:
                fecha = datetime.fromisoformat(fecha_hasta)
                filtros &= Q(fecha_creacion__date__lte=fecha.date())
            except:
                pass

        return filtros

    def _get_queryset(self, filtro):
        return self.model.objects.filter(filtro).order_by('id')
"""


def generate_rest_controller(model_name: str, app_name: str = "carteles"):
    """
    Genera el archivo RestController para un modelo dado.
    """

    ModelName = model_name.capitalize()

    directory = f"output/{model_name}"
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f"{ModelName}RestController.py")

    content = CONTROLLER_TEMPLATE.format(
        model_name=model_name,
        ModelName=ModelName,
        app_name=app_name
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✔ RestController generado: {file_path}")
