
from framework.api.options import BaseOptionsAPIView
from apps.base.models.tipo_documento_identidad import TipoDocumentoIdentidad

class TipoDocumentoIdentidadOptionsView(BaseOptionsAPIView):
    model=TipoDocumentoIdentidad
    url = 'tipo-documento-identidad'
    desc_field = "nombre"
    permisos = [] 