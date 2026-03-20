
from rest_framework import routers
from apps.base.rest_controllers.contacto_rest_controller import (
    ContactoRestController
)

router = routers.SimpleRouter()
router.register(r'contacto', ContactoRestController, 'contacto')

urlpatterns = []

urlpatterns += router.urls
