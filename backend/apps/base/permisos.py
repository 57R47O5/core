from framework.permisos import PermisoManager
from framework.models.basemodels import Constant

class PermisoBase(PermisoManager):
    PERSONA_FISICA_VIEW=Constant("base.persona_fisica.view")
    PERSONA_FISICA_CREATE=Constant("base.persona_fisica.create")
    PERSONA_FISICA_EDIT=Constant("base.persona_fisica.edit")
    PERSONA_FISICA_DESTROY=Constant("base.persona_fisica.destroy")
    PERSONA_JURIDICA_VIEW=Constant("base.persona_juridica.view")
    PERSONA_JURIDICA_CREATE=Constant("base.persona_juridica.create")
    PERSONA_JURIDICA_EDIT=Constant("base.persona_juridica.edit")
    PERSONA_JURIDICA_DESTROY=Constant("base.persona_juridica.destroy")