from django.urls import path
from apps.carteles.views.paciente_view import (
    paciente_detail,
    paciente_list_create,
    paciente_search,
    PacienteNombreOptions
)

from django.urls import path

urlpatterns = [
    path('', paciente_list_create, name='pacientes'),
    path('<int:pk>/', paciente_detail, name='paciente-detail'),
    path('buscar/', paciente_search, name='paciente-search'),
    path('options/', PacienteNombreOptions.as_view(), name='paciente-nombre-options'),
]

