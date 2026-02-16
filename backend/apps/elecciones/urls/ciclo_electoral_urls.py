
from django.urls import path
from apps.elecciones.rest_controllers.ciclo_electoral_rest_controller import (
    CicloElectoralOptionsView as Controller
)

urlpatterns = [
    path(
        Controller.route(),
        Controller.as_view(),
        name=Controller.name()
    ),
]
