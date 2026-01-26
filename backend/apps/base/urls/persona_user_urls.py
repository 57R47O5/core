
from rest_framework import routers
from apps.base.rest_controllers.persona_user_rest_controller import (
    PersonaUserRestController
)

router = routers.SimpleRouter()
router.register(r'persona-user', PersonaUserRestController, 'persona-user')

urlpatterns = []

urlpatterns += router.urls
