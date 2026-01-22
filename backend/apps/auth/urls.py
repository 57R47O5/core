from django.urls import path

from .views.login import login
from .views.logout import LogoutView
from .views.me import MeView
from .views.register import RegisterView

app_name = "auth"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("register/", RegisterView.as_view(), name="register"),
]
