from framework.menu.menu import Node
from framework.permisos import P
from apps.auth.permisos import UserPermisos

MENU = Node(
    "Autenticacion",
    icon="FaKey",
    content=[
        Node(
            label="Nuevo Usuario",
            permiso=P(UserPermisos.CREATE),
            to="register/"
        ),
        Node(
            label="Usuario",
            permiso=P(UserPermisos.CREATE),
            to="user/"
        )
    ]
)