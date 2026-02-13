from framework.menu.menu import Node
from apps.elecciones.rest_controllers.colaborador_rest_controller import ColaboradorRestController
from apps.elecciones.rest_controllers.campana_rest_controller import CampanaRestController
from apps.elecciones.rest_controllers.salida_rest_controller import SalidaRestController
from apps.elecciones.rest_controllers.seccional_rest_controller import SeccionalRestController
from apps.elecciones.rest_controllers.visita_rest_controller import VisitaRestController
from apps.elecciones.rest_controllers.votante_rest_controller import VotanteRestController

MENU = Node(
    "Elecciones",
    icon="FaCheck-To-Slot",
    content=[
        CampanaRestController.to_node(),
        ColaboradorRestController.to_node(),
        SalidaRestController.to_node(),
        SeccionalRestController.to_node(),
        VisitaRestController.to_node(),
        VotanteRestController.to_node(),
    ]
)
