from django.urls import path
from ..views.persona_view import persona_list_create, persona_detail

urlpatterns = [
    path("", persona_list_create, name="persona-list-create"),
    path("<int:pk>/", persona_detail, name="persona-detail"),
]
