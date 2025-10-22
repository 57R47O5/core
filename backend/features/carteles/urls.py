from django.urls import path
from .views.cartel_view import (
    listar_carteles, detalle_cartel, crear_cartel, eliminar_cartel,
    editar_cartel, agregar_imagen_cartel
    
)

urlpatterns = [
    path("carteles/", listar_carteles),
    path("carteles/<int:pk>/", detalle_cartel),
    path("carteles/crear/", crear_cartel),
    path("carteles/<int:pk>/editar/", editar_cartel),
    path("carteles/<int:pk>/eliminar/", eliminar_cartel),
    path("carteles/<int:pk>/imagenes/", agregar_imagen_cartel),
]
