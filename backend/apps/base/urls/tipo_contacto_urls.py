
from django.urls import path
from apps.base.rest_controllers.tipo_contacto_rest_controller import (
    TipoContactoOptionsView
)

urlpatterns = [
    path(r'tipo-contacto/options/', 
        TipoContactoOptionsView.as_view(), 
        name='tipo-contacto-options'),
]


