from ..models.rol import Rol

def user_has_role(user, role_name: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    return role_name in get_roles(user)

def get_roles(user)->list:
    roles = Rol.objects.filter(
        userrole__user=user,
        ).values_list('nombre', flat=True)

    return list(roles)
