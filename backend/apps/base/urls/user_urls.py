from django.urls import path
from apps.base.views.user_views import (
    register_view,
    usuarios_list_create,
    roles_view,
    usuario_detail,
    MedicosOptions,
    )

urlpatterns = [
    path('', usuarios_list_create, name='list'),
    path('<int:pk>/', usuario_detail, name='retrieve'),
    path('register/', register_view, name='register'),
    path('roles/', roles_view, name='roles'),
    path('medicos/options/', MedicosOptions.as_view(), name='usuario-medicos-options'),
]