from apps.base.models.documento_identidad import DocumentoIdentidad
from apps.base.models.contacto import Contacto
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.votante import Votante

class CargaMasivaService():
    
    @classmethod
    def creacion_masiva_votantes(cls, datos:dict):
        pass