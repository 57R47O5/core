from django.db.models import F, Q

from rest_framework import status, viewsets, serializers
from rest_framework.response import Response

from framework.api.options import BaseOptionsAPIView
from apps.base.models.documento_identidad import DocumentoIdentidad
from apps.base.serializers.documento_identidad_serializer import (
    DocumentoIdentidadCreateSerializer,
    DocumentoIdentidadUpdateSerializer,
    DocumentoIdentidadRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class DocumentoIdentidadRestController(ModelRestController):
    model = DocumentoIdentidad
    url='documento-identidad'
    permisos=[]
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
