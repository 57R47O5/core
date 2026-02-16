
from django.urls import path
from apps.elecciones.rest_controllers.estado_salida_rest_controller import (
    EstadoSalidaOptionsView as Controller
)

urlpatterns = [
    path(
        Controller.route(),
        Controller.as_view(),
        name=Controller.name()
    ),
]
