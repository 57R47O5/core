from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.colaborador import Colaborador
from apps.elecciones.serializers.colaborador_serializer import (
    ColaboradorCreateSerializer,
    ColaboradorUpdateSerializer,
    ColaboradorRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosColaborador(PermisoGroup):
    VIEW=Constant("elecciones.colaborador.view")
    CREATE=Constant("elecciones.colaborador.create")
    UPDATE=Constant("elecciones.colaborador.update")
    DESTROY=Constant("elecciones.colaborador.destroy")


class ColaboradorRestController(ModelRestController):
    label = "Colaborador"
    model = Colaborador
    url = "colaborador"
    create_serializer = ColaboradorCreateSerializer
    update_serializer = ColaboradorUpdateSerializer
    retrieve_serializer = ColaboradorRetrieveSerializer    
    permisos = PermisosColaborador

    def serialize_list(self, queryset):
        return list(queryset.values()
                    .annotate(
                        nombres=F("persona__nombres"),
                        apellidos=F("persona__apellidos"),
                    ).annotate(
                        descripcion=Concat(
                        F("nombres"),
                        Value(" "),
                        F("apellidos"),
                        )
                    ).values())
    
    def _get_filter(self, params):
        filtro = Q()
        for key, value in params.items():
            if key in  ['nombres', 'apellidos']:
                filtro &= Q(**{f"persona__{key}__icontains":value})
        return filtro