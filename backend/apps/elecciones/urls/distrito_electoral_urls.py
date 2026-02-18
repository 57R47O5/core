
from django.urls import path
from apps.elecciones.rest_controllers.distrito_electoral_rest_controller import (
    DistritoElectoralOptionsView as Controller
)

urlpatterns = [
    path(
        Controller.route(),
        Controller.as_view(),
        name=Controller.name()
    ),
]
