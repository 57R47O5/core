from django.db import models
from framework.models.basemodels import BaseModel
from apps.base.models.persona import Persona
from apps.base.models.tipo_documento_identidad import TipoDocumentoIdentidad

class DocumentoIdentidad(BaseModel):
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="documentos",
        db_column="persona"
    )

    tipo = models.ForeignKey(
        TipoDocumentoIdentidad, 
        on_delete=models.PROTECT,
        related_name="documentos",
        db_column="tipo"
        )
    numero = models.CharField(max_length=50)
    pais_emision = models.CharField(max_length=2)
    vigente = models.BooleanField(default=True)

    class Meta:
        unique_together = ("tipo", "numero", "pais_emision")
        db_table = "documento_identidad"
        managed = False
