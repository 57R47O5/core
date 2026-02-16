
from django.urls import path
from apps.elecciones.rest_controllers.resultado_visita_rest_controller import (
    ResultadoVisitaOptionsView as Controller
)

urlpatterns = [
    path(
        Controller.route(),
        Controller.as_view(),
        name=Controller.name()
    ),
]
