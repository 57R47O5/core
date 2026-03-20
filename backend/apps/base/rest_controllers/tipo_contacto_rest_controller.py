
from framework.api.options import BaseOptionsAPIView
from apps.base.models.tipo_contacto import TipoContacto

class TipoContactoOptionsView(BaseOptionsAPIView):
    model = TipoContacto
    url='tipo-contacto'
    desc_field='descripcion'
    permisos=[]

