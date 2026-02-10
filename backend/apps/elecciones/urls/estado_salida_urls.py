
from rest_framework import routers
from apps.elecciones.rest_controllers.estado_salida_rest_controller import (
    EstadoSalidaRestController
)

router = routers.SimpleRouter()
router.register(r'estado-salida', EstadoSalidaRestController, 'estado-salida')

urlpatterns = []

urlpatterns += router.urls
