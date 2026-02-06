from apps.auth.models.permiso import PermisoManager
from framework.models.basemodels import Constant

class BasePermisos(PermisoManager):
    PERSONA_FISICA_VIEW=Constant("base.persona_fisica.view")
    PERSONA_FISICA_CREATE=Constant("base.persona_fisica.create")
    PERSONA_FISICA_UPDATE=Constant("base.persona_fisica.update")
    PERSONA_FISICA_DESTROY=Constant("base.persona_fisica.destroy")
    PERSONA_JURIDICA_VIEW=Constant("base.persona_juridica.view")
    PERSONA_JURIDICA_CREATE=Constant("base.persona_juridica.create")
    PERSONA_JURIDICA_UPDATE=Constant("base.persona_juridica.update")
    PERSONA_JURIDICA_DESTROY=Constant("base.persona_juridica.destroy")