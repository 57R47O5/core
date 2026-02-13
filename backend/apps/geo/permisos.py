from apps.auth.models.permiso import PermisoManager
from framework.models.basemodels import Constant
from apps.geo.rest_controllers.lugar_rest_controller import PermisosLugar

class GeoPermisos(PermisoManager):
    grupos = [PermisosLugar]
