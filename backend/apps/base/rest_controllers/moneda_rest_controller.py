from apps.base.models.moneda import Moneda
from apps.base.serializers.moneda_serializer import (
    MonedaCreateSerializer,
    MonedaUpdateSerializer,
    MonedaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class MonedaRestController(ModelRestController):
    model = Moneda
    url='moneda'
    permisos=[]
    create_serializer = MonedaCreateSerializer
    update_serializer = MonedaUpdateSerializer
    retrieve_serializer = MonedaRetrieveSerializer
