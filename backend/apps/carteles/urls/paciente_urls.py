from django.urls import path
from rest_framework import routers
from apps.carteles.views.paciente_view import (
    PacienteNombreOptions,
    PacienteRestController
)

from django.urls import path

router = routers.SimpleRouter()
router.register(r'pacientes', PacienteRestController, 'pacientes')

urlpatterns = [
    path('options/', PacienteNombreOptions.as_view(), name='paciente-nombre-options'),
]

urlpatterns += router.urls



