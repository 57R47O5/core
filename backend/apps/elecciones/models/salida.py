from django.db import models
from framework.exceptions import ExcepcionValidacion
from framework.constantes.mensajes_error import MensajesError
from framework.models.basemodels import BaseModel
from apps.elecciones.models.campana import Campana
from apps.elecciones.models.colaborador import Colaborador
from apps.elecciones.models.estado_salida import EstadoSalida, EstadoSalidaManager

class ErrorSalida(MensajesError):
    NO_CANCELABLE="No se puede cancelar una salida que ya tiene visitas"

class Salida(BaseModel):
    campana = models.ForeignKey(
        Campana,
        on_delete=models.CASCADE,
        related_name="salidas"
    )
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.PROTECT,
        related_name="salidas"
    )
    fecha = models.DateField(auto_created=True)
    estado = models.ForeignKey(EstadoSalida, 
        on_delete=models.PROTECT,
        default=EstadoSalidaManager.EN_CURSO)

    class Meta:
        managed = False
        db_table = "salida"
        constraints = [
            models.UniqueConstraint(
                fields=["colaborador", "fecha"],
                name="uq_salida_colaborador_fecha"
            )
        ]

    def clean(self, *args, **kwargs):
        if self.estado == EstadoSalidaManager.CANCELADA:
            if not self.puede_cancelarse():
                raise ExcepcionValidacion(
                    ErrorSalida.NO_CANCELABLE
                )

    def puede_agregar_visitas(self):
        return self.estado.code == EstadoSalidaManager.EN_CURSO

    def puede_cancelarse(self):
        return not self.visitas.exists()