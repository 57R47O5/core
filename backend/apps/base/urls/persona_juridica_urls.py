
from rest_framework import routers
from apps.base.rest_controllers.persona_juridica_rest_controller import (
    PersonaJuridicaRestController as Controller
)

router = routers.SimpleRouter()
router.register(Controller.url, Controller, Controller.url)

urlpatterns = []

urlpatterns += router.urls
