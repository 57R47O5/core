
from rest_framework import routers
from apps.elecciones.rest_controllers.salida_rest_controller import (
    SalidaRestController
)

router = routers.SimpleRouter()
router.register(r'salida', SalidaRestController, 'salida')

urlpatterns = []

urlpatterns += router.urls
