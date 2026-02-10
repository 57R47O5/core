
from rest_framework import routers
from apps.elecciones.rest_controllers.colaborador_rest_controller import (
    ColaboradorRestController
)

router = routers.SimpleRouter()
router.register(r'colaborador', ColaboradorRestController, 'colaborador')

urlpatterns = []

urlpatterns += router.urls
