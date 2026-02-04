from django.urls import path

from .views.login import LoginView
from .views.logout import LogoutView
from .views.me import MeView
from .views.register import RegisterView
from .views.menu import menu_view

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("menu/",  menu_view, name="menu")
]
