
from rest_framework import routers
from apps.base.rest_controllers.persona_rest_controller import (
    PersonaRestController as Controller
)

router = routers.SimpleRouter()
router.register(Controller.url, Controller, Controller.url)

urlpatterns = []

urlpatterns += router.urls
