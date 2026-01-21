
from rest_framework import routers
from apps.base.rest_controllers.moneda_rest_controller import (
    MonedaRestController
)

router = routers.SimpleRouter()
router.register(r'moneda', MonedaRestController, 'moneda')

urlpatterns = []

urlpatterns += router.urls
