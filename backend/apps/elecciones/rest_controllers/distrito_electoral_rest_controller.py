
from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.distrito_electoral import DistritoElectoral

class DistritoElectoralOptionsView(BaseOptionsAPIView):
    model = DistritoElectoral
    url='distrito-electoral'
    desc_field='Descripcion'
    permisos=[]

