from framework.menu.menu import Node
from apps.base.rest_controllers.persona_fisica_rest_controller import PersonaFisicaRestController
from apps.base.rest_controllers.persona_juridica_rest_controller import PersonaJuridicaRestController

MENU = Node(
    "Base",
    icon="FaBed",
    content=[
        PersonaFisicaRestController.to_node(),
        PersonaJuridicaRestController.to_node(),
    ]
)
