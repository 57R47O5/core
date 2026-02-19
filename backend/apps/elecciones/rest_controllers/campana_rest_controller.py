from django.db.models import F, Value
from django.db.models.functions import Concat
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.campana import Campana
from apps.elecciones.serializers.campana_serializer import (
    CampanaCreateSerializer,
    CampanaUpdateSerializer,
    CampanaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosCampana(PermisoGroup):
    VIEW=Constant("elecciones.campana.view")
    CREATE=Constant("elecciones.campana.create")
    UPDATE=Constant("elecciones.campana.update")
    DESTROY=Constant("elecciones.campana.destroy")


class CampanaRestController(ModelRestController):
    label = "Campana"
    model = Campana
    url = "campana"
    create_serializer = CampanaCreateSerializer
    update_serializer = CampanaUpdateSerializer
    retrieve_serializer = CampanaRetrieveSerializer    
    permisos = PermisosCampana

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        return list(queryset.values().annotate(
            candidato=Concat(
                        F("candidato__nombres"),
                        Value(" "),
                        F("candidato__apellidos")),
            distrito=F("distrito__nombre"),
            ciclo=F("ciclo__nombre"),
                        ).values()
                        )
