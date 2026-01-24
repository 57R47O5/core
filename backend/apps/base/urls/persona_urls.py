
from rest_framework import routers
from apps.base.rest_controllers.persona_rest_controller import (
    PersonaRestController
)

router = routers.SimpleRouter()
router.register(r'persona', PersonaRestController, 'persona')

urlpatterns = []

urlpatterns += router.urls
