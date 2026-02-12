from django.urls import path
from rest_framework import routers
from apps.base.rest_controllers.tipo_documento_identidad_rest_controller import (
    TipoDocumentoIdentidadOptionsView as Controller, 
)

urlpatterns = [
    path(
        Controller.route(),
        Controller.as_view(),
        name=Controller.name()
    ),
]

