from django.urls import path
from rest_framework import routers
from apps.base.rest_controllers.tipo_documento_identidad_rest_controller import (
    TipoDocumentoIdentidadRestController as Controller, 
    TipoDocumentoIdentidadOptionsView
)

router = routers.SimpleRouter()
router.register(Controller.url, Controller, Controller.url)

urlpatterns = [
    path(r'tipo-documento-identidad/options/', TipoDocumentoIdentidadOptionsView.as_view(), name='tipo-documento-identidad-options'),
]

urlpatterns += router.urls
