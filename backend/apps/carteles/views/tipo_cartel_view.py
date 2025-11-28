from apps.base.framework.api.options import BaseOptionsAPIView
from apps.carteles.models.tipocartel import TipoCartel

class TipoCartelOptions(BaseOptionsAPIView):
    model = TipoCartel
    id_field = "pk"
    desc_field = "nombre"  
    order_by = "id"