from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.salida import Salida
from apps.elecciones.serializers.salida_serializer import (
    SalidaCreateSerializer,
    SalidaUpdateSerializer,
    SalidaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController, Capability, CapabilitySet
class PermisosSalida(PermisoGroup):
    VIEW=Constant("elecciones.salida.view")
    CREATE=Constant("elecciones.salida.create")
    UPDATE=Constant("elecciones.salida.update")
    DESTROY=Constant("elecciones.salida.destroy")
    ESTADO_SALIDA_VIEW=Constant("elecciones.estado_salida.view")

class SalidaRestController(ModelRestController):
    label = "Salidas"
    model = Salida
    url = "salida"
    create_serializer = SalidaCreateSerializer
    update_serializer = SalidaUpdateSerializer
    retrieve_serializer = SalidaRetrieveSerializer    
    permisos = PermisosSalida

    capabilities = CapabilitySet(
        Capability(
            name="agregar_visitas",
            business_rule=lambda instancia: instancia.puede_agregar_visitas
        )
    )

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        model=queryset.model
        salida = list(queryset.values().annotate(
            colaborador=F("colaborador__persona__nombres"), 
            estado=F("estado__codigo"),
        ).annotate(
            descripcion=Concat(
                F("colaborador"), Value(" - "), F("estado"), output_field=CharField()
            )
        ).values())
        return salida
