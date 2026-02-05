
from rest_framework import routers
from apps.base.rest_controllers.documento_identidad_rest_controller import (
    DocumentoIdentidadRestController as Controller
)

router = routers.SimpleRouter()
router.register(Controller.url, Controller, Controller.url)

urlpatterns = []

urlpatterns += router.urls
