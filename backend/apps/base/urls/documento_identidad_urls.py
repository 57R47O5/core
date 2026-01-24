
from rest_framework import routers
from apps.base.rest_controllers.documento_identidad_rest_controller import (
    DocumentoIdentidadRestController
)

router = routers.SimpleRouter()
router.register(r'documento-identidad', DocumentoIdentidadRestController, 'documento-identidad')

urlpatterns = []

urlpatterns += router.urls
