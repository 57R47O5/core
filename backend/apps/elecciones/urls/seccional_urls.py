
from rest_framework import routers
from apps.elecciones.rest_controllers.seccional_rest_controller import (
    SeccionalRestController
)

router = routers.SimpleRouter()
router.register(r'seccional', SeccionalRestController, 'seccional')

urlpatterns = []

urlpatterns += router.urls
