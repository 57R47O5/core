
from rest_framework import routers
from apps.base.rest_controllers.persona_fisica_rest_controller import (
    PersonaFisicaRestController
)

router = routers.SimpleRouter()
router.register(r'persona-fisica', PersonaFisicaRestController, 'persona-fisica')

urlpatterns = []

urlpatterns += router.urls
