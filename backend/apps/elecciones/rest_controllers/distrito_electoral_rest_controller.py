from apps.elecciones.models.distrito_electoral import DistritoElectoral
from controllers.base.base_rest_controller import ModelRestController
from apps.elecciones.serializers.distrito_electoral_serializer import (
    DistritoElectoralCreateSerializer,
    DistritoElectoralRetrieveSerializer,
    DistritoElectoralUpdateSerializer
)

class DistritoElectoralRestController(ModelRestController):
    label = "Distrito Electoral"
    model = DistritoElectoral
    url='distrito-electoral'
    desc_field='descripcion'
    create_serializer = DistritoElectoralCreateSerializer
    update_serializer = DistritoElectoralUpdateSerializer
    retrieve_serializer = DistritoElectoralRetrieveSerializer    

    permisos=[]


