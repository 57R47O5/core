from rest_framework import routers

router = routers.SimpleRouter()

from apps.base.rest_controllers.moneda_rest_controller import MonedaRestController

router.register(r'moneda', MonedaRestController, 'moneda')

urlpatterns = router.urls
