
from rest_framework import routers
from apps.elecciones.rest_controllers.resultado_visita_rest_controller import (
    ResultadoVisitaRestController
)

router = routers.SimpleRouter()
router.register(r'resultado-visita', ResultadoVisitaRestController, 'resultado-visita')

urlpatterns = []

urlpatterns += router.urls
