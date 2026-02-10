
from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.resultado_visita import ResultadoVisita

class ResultadoVisitaOptionsView(BaseOptionsAPIView):
    model = ResultadoVisita
    url='resultado-visita'
    desc_field='Descripcion'
    permisos=[]

