from django.urls import path
from rest_framework import routers

from .views.login import LoginView
from .views.logout import LogoutView
from .views.me import MeView
from .views.register import RegisterView, UserListView
from .views.menu import menu_view
from .rest_controllers.user_rest_controller import UserRestController 
from .rest_controllers.rol_rest_controller import RolRestController, RolOptionsView 
from .rest_controllers.permiso_rest_controller import PermisoRestController 
from .rest_controllers.user_rol_rest_controller import UserRolRestController 
from .rest_controllers.rol_permiso_rest_controller import RolPermisoRestController 

app_name = "auth"

router = routers.SimpleRouter()
router.register(UserRestController.url, UserRestController, UserRestController.url)
router.register(RolRestController.url, RolRestController, RolRestController.url)
router.register(PermisoRestController.url, PermisoRestController, PermisoRestController.url)
router.register(UserRolRestController.url, UserRolRestController, UserRolRestController.url)
router.register(RolPermisoRestController.url, RolPermisoRestController, RolPermisoRestController.url)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("menu/",  menu_view, name="menu"),
    path("users/", UserListView.as_view(), name="users"),
    path(RolOptionsView.route(), RolOptionsView.as_view(), name=RolOptionsView.name())    
]

urlpatterns += router.urls