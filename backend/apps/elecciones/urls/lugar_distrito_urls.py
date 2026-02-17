
from rest_framework import routers
from apps.elecciones.rest_controllers.lugar_distrito_rest_controller import (
    LugarDistritoRestController as Controller
)

router = routers.SimpleRouter()
router.register(r'lugar-distrito', Controller, 'lugar-distrito')

urlpatterns = []

urlpatterns += router.urls
