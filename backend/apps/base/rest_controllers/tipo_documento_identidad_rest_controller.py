from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.base.models.tipo_documento_identidad import TipoDocumentoIdentidad
from apps.base.serializers.tipo_documento_identidad_serializer import (
    TipoDocumentoIdentidadCreateSerializer,
    TipoDocumentoIdentidadUpdateSerializer,
    TipoDocumentoIdentidadRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class TipoDocumentoIdentidadRestController(ModelRestController):
    url = 'tipo-documento-identidad'
    permisos = [] 
    model = TipoDocumentoIdentidad
    create_serializer = TipoDocumentoIdentidadCreateSerializer
    update_serializer = TipoDocumentoIdentidadUpdateSerializer
    retrieve_serializer = TipoDocumentoIdentidadRetrieveSerializer

class TipoDocumentoIdentidadOptionsView(BaseOptionsAPIView):
    model=TipoDocumentoIdentidad
    url = 'tipo-documento-identidad'
    desc_field = "nombre"
    permisos = [] 