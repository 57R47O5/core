from django.db import models
from django.db.models import F
from framework.models.basemodels import BaseModel
from framework.exceptions import  ExcepcionValidacion
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.campana import Campana


class Colaborador(BaseModel):
    persona = models.ForeignKey(PersonaFisica, 
        on_delete=models.CASCADE, db_column='persona')
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, 
        related_name='colaboradores', db_column='campana')

    class Meta:
        managed=False
        db_table="colaborador"

    constraints = [
        models.UniqueConstraint(
            fields=["persona", "campana"],
            name="uq_colaborador_persona_campana")
        ]

    def __str__(self):
        return f"{str(self.persona)} - {self.campana}"
    
    def clean(self, *args, **kwargs):
        if not self.campana_id:
            raise ExcepcionValidacion("No hay campaña activa.")

    def save(self, *args, **kwargs):
        self.clean(*args, **kwargs)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.salidas.exists():
            raise ExcepcionValidacion("No se puede eliminar colaborador con salidas")
        self.persona.delete()
        super().delete(*args, **kwargs)
    
    @property
    def usuario_agregable(self):
        return not self.persona.tiene_usuario
    
    @property
    def user(self):
        usuarios = self.persona.persona.usuarios.all()
        if usuarios.exists():
            usuario = usuarios.first().user
        user_serializado = {
            "id": usuario.pk,
            "label": usuario.username,
            "controller": "user"
        } if  usuarios.exists() else None
        return user_serializado
    
    @property
    def salida(self):
        datos_salida = self.salidas.all().values(
            ).annotate(estado_salida=F("estado__codigo")).values()
        for dato in datos_salida:
            dato["salida"]={"url":f"salida/{self.pk}", "label":self.pk}
        return datos_salida
