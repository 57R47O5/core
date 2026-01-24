
from rest_framework import routers
from apps.base.rest_controllers.persona_juridica_rest_controller import (
    PersonaJuridicaRestController
)

router = routers.SimpleRouter()
router.register(r'persona-juridica', PersonaJuridicaRestController, 'persona-juridica')

urlpatterns = []

urlpatterns += router.urls
