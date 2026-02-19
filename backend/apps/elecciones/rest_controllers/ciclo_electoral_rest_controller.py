
from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.ciclo_electoral import CicloElectoral

class CicloElectoralOptionsView(BaseOptionsAPIView):
    model = CicloElectoral
    url='ciclo-electoral'
    desc_field='descripcion'
    permisos=[]

