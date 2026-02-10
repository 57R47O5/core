
from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.estado_salida import EstadoSalida

class EstadoSalidaOptionsView(BaseOptionsAPIView):
    model = EstadoSalida
    url='estado-salida'
    desc_field='Descripcion'
    permisos=[]

