from django.db.models import F, Q

from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant
from apps.base.models.documento_identidad import DocumentoIdentidad
from apps.base.serializers.documento_identidad_serializer import (
    DocumentoIdentidadCreateSerializer,
    DocumentoIdentidadUpdateSerializer,
    DocumentoIdentidadRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosDocumentoIdentidad(PermisoGroup):
    VIEW=Constant("base.documento_identidad.view")
    CREATE=Constant("base.documento_identidad.create")
    UPDATE=Constant("base.documento_identidad.update")
    DESTROY=Constant("base.documento_identidad.destroy")
class DocumentoIdentidadRestController(ModelRestController):
    label = "Documento Identidad"
    model = DocumentoIdentidad
    url='documento-identidad'
    permisos=PermisosDocumentoIdentidad
    create_serializer = DocumentoIdentidadCreateSerializer
    update_serializer = DocumentoIdentidadUpdateSerializer
    retrieve_serializer = DocumentoIdentidadRetrieveSerializer

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        return list(queryset.values().annotate(
            tipo=F("tipo_id")
        ).values())
    
    def _get_filter(self, params):
        filtro = Q()
        for key, value in params.items():
            filtro &= Q(**{key: value})
        return filtro
    
    def _get_queryset(self, filtro):
        return self.model.objects.filter(filtro)
