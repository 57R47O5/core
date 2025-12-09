from django.urls import path
from apps.carteles.views.turno_view import (
    TurnoEstadosOptions,
    turno_create,
    turno_detail,
    turnos
)

urlpatterns = [
    path("estados/", TurnoEstadosOptions.as_view(), name="turnos-estados"),
    path("", turnos, name="turnos"),
    path("nuevo/", turno_create, name="turno-create"),
    path("<int:pk>/", turno_detail, name="turno-detail"),
]
