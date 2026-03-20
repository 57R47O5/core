from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from apps.elecciones.models.distrito_electoral import DistritoElectoral
from controllers.base.base_rest_controller import BaseRestController, ModelRestController
from apps.elecciones.serializers.distrito_electoral_serializer import (
    DistritoElectoralCreateSerializer,
    DistritoElectoralRetrieveSerializer,
    DistritoElectoralUpdateSerializer
)
from apps.elecciones.services.distrito_service import DistritoGeoImportService
from framework.exceptions import excepcion
from rest_framework.parsers import MultiPartParser, FormParser


class DistritoElectoralRestController(ModelRestController):
    label = "Distrito Electoral"
    model = DistritoElectoral
    url='distrito-electoral'
    desc_field='descripcion'
    create_serializer = DistritoElectoralCreateSerializer
    update_serializer = DistritoElectoralUpdateSerializer
    retrieve_serializer = DistritoElectoralRetrieveSerializer
    parser_classes = [MultiPartParser, FormParser]
    

    permisos=[]

    @excepcion
    def create(self, request):
        datos=request.data.copy()
        service = DistritoGeoImportService
        instancia = service.crear_distrito(datos.get("documento"))
        return Response({"Creación exitosa"}, status=status.HTTP_201_CREATED)