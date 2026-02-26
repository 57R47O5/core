from framework.menu.menu import Node
from apps.geo.rest_controllers.lugar_rest_controller import LugarRestController

MENU = Node(
    "Geografia",
    icon="FaMapMarkerAlt",
    content=[
        LugarRestController.to_node()
    ]
)