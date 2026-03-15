from rest_framework import routers
from apps.elecciones.rest_controllers.analitica_rest_controller import (
    AnaliticaRestController)

router = routers.SimpleRouter()
router.register(r'analitica', AnaliticaRestController, 'analitica')

urlpatterns = []

urlpatterns += router.urls
