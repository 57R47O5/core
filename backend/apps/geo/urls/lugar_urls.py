from rest_framework import routers
from apps.geo.rest_controllers.lugar_rest_controller import LugarRestController as Controller

router = routers.SimpleRouter()
router.register(Controller.url, Controller, Controller.url)

urlpatterns = []
urlpatterns += router.urls
