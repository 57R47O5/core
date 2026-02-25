
from rest_framework import routers
from apps.elecciones.rest_controllers.distrito_electoral_rest_controller import (
    DistritoElectoralRestController as Controller
)

router = routers.SimpleRouter()
router.register(r'distrito-electoral', Controller, 'distrito-electoral')

urlpatterns = []

urlpatterns += router.urls
