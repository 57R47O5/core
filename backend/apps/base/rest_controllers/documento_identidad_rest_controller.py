from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.base.models.documento_identidad import DocumentoIdentidad
from apps.base.serializers.documento_identidad_serializer import (
    DocumentoIdentidadCreateSerializer,
    DocumentoIdentidadUpdateSerializer,
    DocumentoIdentidadRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class DocumentoIdentidadRestController(ModelRestController):
    model = DocumentoIdentidad
    create_serializer = DocumentoIdentidadCreateSerializer
    update_serializer = DocumentoIdentidadUpdateSerializer
    retrieve_serializer = DocumentoIdentidadRetrieveSerializer
