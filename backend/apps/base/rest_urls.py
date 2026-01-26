from rest_framework import routers

router = routers.SimpleRouter()

from apps.base.rest_controllers.documento_identidad_rest_controller import DocumentoIdentidadRestController
from apps.base.rest_controllers.moneda_rest_controller import MonedaRestController
from apps.base.rest_controllers.persona_fisica_rest_controller import PersonaFisicaRestController
from apps.base.rest_controllers.persona_juridica_rest_controller import PersonaJuridicaRestController
from apps.base.rest_controllers.persona_rest_controller import PersonaRestController
from apps.base.rest_controllers.persona_user_rest_controller import PersonaUserRestController
from apps.base.rest_controllers.tipo_documento_identidad_rest_controller import TipoDocumentoIdentidadRestController

router.register(r'documento-identidad', DocumentoIdentidadRestController, 'documento-identidad')
router.register(r'moneda', MonedaRestController, 'moneda')
router.register(r'persona-fisica', PersonaFisicaRestController, 'persona-fisica')
router.register(r'persona-juridica', PersonaJuridicaRestController, 'persona-juridica')
router.register(r'persona', PersonaRestController, 'persona')
router.register(r'persona-user', PersonaUserRestController, 'persona-user')
router.register(r'tipo-documento-identidad', TipoDocumentoIdentidadRestController, 'tipo-documento-identidad')

urlpatterns = router.urls
