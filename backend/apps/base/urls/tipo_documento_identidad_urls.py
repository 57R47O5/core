from django.urls import path
from rest_framework import routers
from apps.base.rest_controllers.tipo_documento_identidad_rest_controller import (
    TipoDocumentoIdentidadRestController, 
    TipoDocumentoIdentidadOptionsView
)

router = routers.SimpleRouter()
router.register(r'tipo-documento-identidad', TipoDocumentoIdentidadRestController, 'tipo-documento-identidad')

urlpatterns = [
    path('options/', TipoDocumentoIdentidadOptionsView.as_view(), name='tipo-documento-identidad-options'),
]

urlpatterns += router.urls
