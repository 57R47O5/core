from apps.auth.models.user import User
from framework.menu.menu import generar_menu

def get_menu_for(user:User):
    return generar_menu(user.permisos)