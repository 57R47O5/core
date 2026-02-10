from django.db import models
from framework.exceptions import ExcepcionValidacion
from framework.constantes.mensajes_error import MensajesError
from apps.geo.models.lugar import Punto
from apps.elecciones.models.salida import Salida
from apps.elecciones.models.votante import Votante
from apps.elecciones.models.resultado_visita import ResultadoVisita

class ErrorVisita(MensajesError):
    NO_REGISTRABLE="No se pueden registrar visitas si la salida no está en curso"

class Visita(models.Model):
    """
    Registro de cada visita. Se autoregistra fecha y ubicación (si la app la provee).
    - notes: texto libre
    """
    salida = models.ForeignKey(
        Salida,
        on_delete=models.CASCADE,
        related_name="visitas"
    )
    votante = models.ForeignKey(Votante, on_delete=models.PROTECT, related_name='visitas')
    lugar = models.ForeignKey(Punto, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    resultado = models.ForeignKey(ResultadoVisita, on_delete=models.PROTECT)
    notas = models.TextField(null=True, blank=True)

    class Meta:
        managed=False
        db_table="visita"

    def __str__(self):
        return f"Visita a {self.votante} por {self.colaborador} el ({self.fecha.isocalendar()})"

    def clean(self):
        if self._state.adding is True:
            if not self.salida.puede_agregar_visitas():
                raise ExcepcionValidacion(
                    ErrorVisita.NO_REGISTRABLE
                )
