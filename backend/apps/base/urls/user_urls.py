from django.urls import path
from apps.base.views.user_views import (
    register_view,
    usuarios_list_create,
    usuario_detail,
    UserRolesOptions,
    MedicosOptions,
    )

urlpatterns = [
    path('', usuarios_list_create, name='list'),
    path('<int:pk>/', usuario_detail, name='retrieve'),
    path('register/', register_view, name='register'),
    path('roles/options/', UserRolesOptions.as_view(), name='usuario-roles-options'),
    path('medicos/options/', MedicosOptions.as_view(), name='usuario-medicos-options'),
]