from framework.menu.menu import Node
from framework.permisos import P
from apps.auth.permisos import AuthPermisos

MENU = Node(
    "Autenticacion",
    icon="FaKey",
    content=[
        Node(
            label="Registro",
            permiso=P(AuthPermisos.REGISTER),
            to="register/"
        )
    ]
)