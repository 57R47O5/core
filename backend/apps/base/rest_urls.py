from rest_framework import routers

router = routers.SimpleRouter()

from apps.base.rest_controllers.moneda_rest_controller import MonedaRestController
from apps.base.rest_controllers.user_rol_rest_controller import UserRolRestController

router.register(r'moneda', MonedaRestController, 'moneda')
router.register(r'user-rol', UserRolRestController, 'user-rol')

urlpatterns = router.urls
