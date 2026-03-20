
from django.urls import path
from rest_framework import routers
from apps.elecciones.rest_controllers.votante_rest_controller import (
    VotanteRestController, VotantesOptionsAPIView
)

router = routers.SimpleRouter()
router.register(r'votante', VotanteRestController, 'votante')

urlpatterns = [
    path(r'votantes/options/', 
        VotantesOptionsAPIView.as_view(), 
        name="votantes-options"),
]

urlpatterns += router.urls
