
from rest_framework import routers
from apps.base.rest_controllers.tipo_contacto_rest_controller import (
    TipoContactoRestController
)

router = routers.SimpleRouter()
router.register(r'tipo-contacto', TipoContactoRestController, 'tipo-contacto')

urlpatterns = []

urlpatterns += router.urls
