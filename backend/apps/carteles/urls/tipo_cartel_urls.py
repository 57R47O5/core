from django.urls import path
from ..views.tipo_cartel_view import TipoCartelOptions

urlpatterns = [
    path("options/", TipoCartelOptions.as_view(), name="tipo-cartel-options")
]