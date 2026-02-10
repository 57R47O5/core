
from rest_framework import routers
from apps.elecciones.rest_controllers.votante_rest_controller import (
    VotanteRestController
)

router = routers.SimpleRouter()
router.register(r'votante', VotanteRestController, 'votante')

urlpatterns = []

urlpatterns += router.urls
