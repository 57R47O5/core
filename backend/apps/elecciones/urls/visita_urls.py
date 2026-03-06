
from rest_framework import routers
from apps.elecciones.rest_controllers.visita_rest_controller import (
    VisitaRestController
)

router = routers.SimpleRouter()
router.register(r'visita', VisitaRestController, 'visita')

urlpatterns = []

urlpatterns += router.urls
