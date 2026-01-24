
from rest_framework import routers
from apps.base.rest_controllers.tipo_documento_identidad_rest_controller import (
    TipoDocumentoIdentidadRestController
)

router = routers.SimpleRouter()
router.register(r'tipo-documento-identidad', TipoDocumentoIdentidadRestController, 'tipo-documento-identidad')

urlpatterns = []

urlpatterns += router.urls
