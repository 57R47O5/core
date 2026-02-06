from apps.auth.models.user import User
from apps.auth.models.permiso import Permiso
from framework.menu.menu import generar_menu

def get_menu_for(user:User):
    if "Owner" in user.roles:
        permisos = []
        for permiso in Permiso.objects.all():
            permisos.append(permiso)
    else:
        permisos=user.permisos
    return generar_menu(permisos)