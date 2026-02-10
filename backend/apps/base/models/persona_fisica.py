from django.db import models
from framework.models.basemodels import BaseModel
from apps.base.models.persona import Persona

class PersonaFisica(BaseModel):
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name="fisica",
        db_column='persona',
    )

    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "persona_fisica"
        managed = False    

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}".strip()

    def __str__(self):
        return f"{self.nombre_completo}"
    
    @property
    def documentos_identidad(self):
        documentos_identidad = self.persona.documentos.all().values("tipo", "numero")
        return documentos_identidad
    
    def delete(self, *args, **kwargs):
        persona=self.persona
        super().delete(*args, **kwargs)
        documentos=persona.documentos.all()
        for documento in documentos:
            documento.delete()
        persona.delete()
        return True
