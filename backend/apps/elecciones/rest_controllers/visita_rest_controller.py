from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.visita import Visita
from apps.elecciones.serializers.visita_serializer import (
    VisitaRetrieveSerializer, VisitaCreateSerializer, VisitaUpdateSerializer
)
from controllers.base.base_rest_controller import ModelRestController

class PermisosVisita(PermisoGroup):
    VIEW=Constant("elecciones.visita.view")
    CREATE=Constant("elecciones.visita.create")
    UPDATE=Constant("elecciones.visita.update")
    DESTROY=Constant("elecciones.visita.destroy")
    RESULTADO_VISITA_VIEW=Constant("elecciones.resultado_visita.view")

class VisitaRestController(ModelRestController):
    label = "Visita"
    model = Visita
    url = "visita"  
    permisos = PermisosVisita
    create_serializer = VisitaCreateSerializer
    update_serializer = VisitaUpdateSerializer
    retrieve_serializer = VisitaRetrieveSerializer

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        model = queryset.model
        if hasattr(model, "descripcion_expression") and \
            not hasattr(model, "descripcion"):
            queryset = queryset.annotate(
                descripcion=model.descripcion_expression()
            )           
        salida = list(queryset.values().annotate(
            salida=Concat(F("salida__colaborador__persona__nombres"), 
            Value(" "), 
            F("salida__fecha"), output_field=CharField()
            ),
            resultado=F("resultado__descripcion"),
            votante=Concat(
                F("votante__persona__nombres"),
                Value(" "),
                F("votante__persona__apellidos"),
            ),
            latitud=F("lugar__centroide_lat"),
            longitud=F("lugar__centroide_lon"),
        ).annotate(
            descripcion=Concat(F("salida"), Value("-"), F("votante"))
        ).values())
        return salida
    
    def _serialize_instance(self, request, instancia):
        salida_serializada = super()._serialize_instance(request, instancia)
        salida_serializada["lugar"]["ltlng"]={
            "lat":salida_serializada["lugar"]["centroide_lat"], 
            "lng":salida_serializada["lugar"]["centroide_lon"]}
        salida_serializada["lugar"]["lat"]=salida_serializada["lugar"]["centroide_lat"]
        salida_serializada["lugar"]["lon"]=salida_serializada["lugar"]["centroide_lon"]
        return salida_serializada