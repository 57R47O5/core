
from rest_framework import routers
from apps.base.rest_controllers.moneda_rest_controller import (
    MonedaRestController as Controller
)

router = routers.SimpleRouter()
router.register(Controller.url, Controller, Controller.url)

urlpatterns = []

urlpatterns += router.urls
