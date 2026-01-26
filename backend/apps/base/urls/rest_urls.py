from rest_framework import routers

router = routers.SimpleRouter()

from apps.base.rest_controllers.moneda_rest_controller import MonedaRestController
from apps.base.rest_controllers.persona_rest_controller import PersonaRestController
from apps.base.rest_controllers.persona_fisica_rest_controller import PersonaFisicaRestController
from apps.base.rest_controllers.persona_juridica_rest_controller import PersonaJuridicaRestController
from apps.base.rest_controllers.tipo_documento_identidad_rest_controller import TipoDocumentoIdentidadRestController
from apps.base.rest_controllers.documento_identidad_rest_controller import DocumentoIdentidadRestController

router.register(r'moneda', MonedaRestController, 'moneda')
router.register(r'persona', PersonaRestController, 'persona')
router.register(r'persona-fisica', PersonaFisicaRestController, 'persona-fisica')
router.register(r'persona-juridica', PersonaJuridicaRestController,'persona-juridica')
router.register(r'tipo-documento-identidad', TipoDocumentoIdentidadRestController,'tipo-documento-identidad')
router.register(r'documento-identidad', DocumentoIdentidadRestController,'documento-identidad')

urlpatterns = router.urls
