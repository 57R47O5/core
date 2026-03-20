from django.db import models
from .persona import Persona
from .tipo_contacto import TipoContacto
from framework.models.basemodels import BaseModel

class Contacto(BaseModel):
    '''
    Modelo utilizado para almacenar los contactos de una persona, ya sea física o jurídica.

    Los contactos pueden ser de tipo correo electrónico, teléfono o dirección.
    '''
    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name='contactos', db_column="persona")  
    tipo = models.ForeignKey(
        TipoContacto, on_delete=models.PROTECT, related_name='contactos', db_column="tipo")
    valor = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = "contacto"
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"