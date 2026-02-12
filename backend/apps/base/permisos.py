from apps.auth.models.permiso import PermisoManager, PermisoGroup
from framework.models.basemodels import Constant

class PermisosPersonaFisica(PermisoGroup):
    VIEW=Constant("base.persona_fisica.view")
    CREATE=Constant("base.persona_fisica.create")
    UPDATE=Constant("base.persona_fisica.update")
    DESTROY=Constant("base.persona_fisica.destroy")

class PermisosPersonaJuridica(PermisoGroup):
    VIEW=Constant("base.persona_juridica.view")
    CREATE=Constant("base.persona_juridica.create")
    UPDATE=Constant("base.persona_juridica.update")
    DESTROY=Constant("base.persona_juridica.destroy")

class BasePermisos(PermisoManager):
    grupos = [
        PermisosPersonaFisica,
        PermisosPersonaJuridica
    ]