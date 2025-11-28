from django.urls import path
from apps.base.views.user_views import (
    register_view,
    usuarios_list_create,
    usuario_retrieve_update,
    UserRolesOptions
    )

urlpatterns = [
    path('', usuarios_list_create, name='list'),
    path('<int:pk>/', usuario_retrieve_update, name='retrieve'),
    path('register/', register_view, name='register'),
    path('roles/options/', UserRolesOptions.as_view(), name='usuario-roles-options'),
]