from apps.auth.models.permiso import PermisoManager, PermisoGroup
from framework.models.basemodels import Constant

class PermisosColaborador(PermisoGroup):
    VIEW=Constant("elecciones.colaborador.view")
    CREATE=Constant("elecciones.colaborador.create")
    UPDATE=Constant("elecciones.colaborador.update")
    DESTROY=Constant("elecciones.colaborador.destroy")
class PermisosCampana(PermisoGroup):
    VIEW=Constant("elecciones.campana.view")
    CREATE=Constant("elecciones.campana.create")
    UPDATE=Constant("elecciones.campana.update")
    DESTROY=Constant("elecciones.campana.destroy")

class PermisosSalida(PermisoGroup):
    VIEW=Constant("elecciones.salida.view")
    CREATE=Constant("elecciones.salida.create")
    UPDATE=Constant("elecciones.salida.update")
    DESTROY=Constant("elecciones.salida.destroy")
    ESTADO_SALIDA_VIEW=Constant("elecciones.estado_salida.view")

class PermisosSeccional(PermisoGroup):
    VIEW=Constant("elecciones.seccional.view")
    CREATE=Constant("elecciones.seccional.create")
    UPDATE=Constant("elecciones.seccional.update")
    DESTROY=Constant("elecciones.seccional.destroy")

class PermisosVisita(PermisoGroup):
    VIEW    = Constant("elecciones.visita.view")
    CREATE  = Constant("elecciones.visita.create")
    UPDATE  = Constant("elecciones.visita.update")
    DESTROY = Constant("elecciones.visita.destroy")
    RESULTADO_VISITA_VIEW=Constant("elecciones.resultado_visita.view")

class PermisosVotante(PermisoGroup):
    VIEW=Constant("elecciones.votante.view")
    CREATE=Constant("elecciones.votante.create")
    UPDATE=Constant("elecciones.votante.update")
    DESTROY=Constant("elecciones.votante.destroy")

class EleccionesPermisos(PermisoManager):
    '''
    Estos son todos los permisos que se utilizan para elecciones
    '''
    grupos = [
        PermisosColaborador,
        PermisosCampana,
        PermisosSalida,
        PermisosSeccional,
        PermisosVisita,
        PermisosVotante
    ] 
    
