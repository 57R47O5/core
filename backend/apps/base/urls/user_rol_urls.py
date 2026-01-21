
from django.urls import path
from rest_framework import routers
from apps.base.rest_controllers.user_rol_rest_controller import (
    UserRolRestController
)

router = routers.SimpleRouter()
router.register(r'user-rol', UserRolRestController, 'user-rol')

urlpatterns = []

urlpatterns += router.urls
