
from rest_framework import routers
from apps.elecciones.rest_controllers.campana_rest_controller import (
    CampanaRestController
)

router = routers.SimpleRouter()
router.register(r'campana', CampanaRestController, 'campana')

urlpatterns = []

urlpatterns += router.urls
