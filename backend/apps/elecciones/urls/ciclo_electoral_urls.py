
from rest_framework import routers
from apps.elecciones.rest_controllers.ciclo_electoral_rest_controller import (
    CicloElectoralRestController
)

router = routers.SimpleRouter()
router.register(r'ciclo-electoral', CicloElectoralRestController, 'ciclo-electoral')

urlpatterns = []

urlpatterns += router.urls
