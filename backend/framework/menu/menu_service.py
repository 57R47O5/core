from apps.auth.models.user import User
from apps.auth.models.rol import RolManager
from apps.auth.models.permiso import Permiso
from framework.menu.menu import generar_menu

def get_menu_for(user:User):
    permisos=user.permisos
    if user.roles.contains(RolManager.OWNER):
        permisos=Permiso.objects.all()
    return generar_menu(permisos)