from framework.menu.menu import Node
from apps.geo.rest_controllers.lugar_rest_controller import LugarRestController

MENU = Node(
    "Geografia",
    icon="FaEarth-America",
    content=[
        LugarRestController.to_node()
    ]
)