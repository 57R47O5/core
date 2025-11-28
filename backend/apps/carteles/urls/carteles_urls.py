from django.urls import path
from ..views.cartel_view import (
    listar_carteles, detalle_cartel, crear_cartel, eliminar_cartel,
    editar_cartel, agregar_imagen_cartel
)

urlpatterns = [
    path("", listar_carteles),
    path("<int:pk>/", detalle_cartel),
    path("crear/", crear_cartel),
    path("<int:pk>/editar/", editar_cartel),
    path("<int:pk>/eliminar/", eliminar_cartel),
    path("<int:pk>/imagenes/", agregar_imagen_cartel),
]
