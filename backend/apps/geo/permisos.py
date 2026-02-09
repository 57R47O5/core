from apps.auth.models.permiso import PermisoManager
from framework.models.basemodels import Constant

class GeoPermisos(PermisoManager):
    LUGAR_VIEW=Constant("geo.lugar.view")
    LUGAR_CREATE=Constant("geo.lugar.create")
    LUGAR_UPDATE=Constant("geo.lugar.update")
    LUGAR_DESTROY=Constant("geo.lugar.destroy")
