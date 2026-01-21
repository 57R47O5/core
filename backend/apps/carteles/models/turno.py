from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from backend.apps.auth.models.user import User
from apps.carteles.models.paciente import Paciente

class Turno(models.Model):
    '''
    Un turno siempre corresponde a un  médico y un  paciente
    No se pueden agendar más de un turno para el mismo médico a la misma  hora
    '''

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmado", "Confirmado"),
        ("cancelado", "Cancelado"),
    ]
    DURACION_TURNO=30

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    odontologo = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"rol": "medico"})
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["fecha_inicio"]
        unique_together = ("odontologo", "fecha_inicio")

    def clean(self):
        # completar fecha_fin si no se envía
        if not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(minutes=self.DURACION_TURNO)

        # validar solapamiento
        overlapping = Turno.objects.filter(
            odontologo=self.odontologo,
            fecha_inicio__lt=self.fecha_fin,
            fecha_fin__gt=self.fecha_inicio,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("El turno se solapa con otro turno existente.")

    def save(self, *args, **kwargs):
        '''
        Guarda un turno
        Realiza validaciones
        Si no se definió una hora de finalización, la define 
        
        :param self: Instancia de Turno
        '''
        self.full_clean()
        if self._state.adding is True:
            if not self.fecha_fin:
                self.fecha_fin=self.fecha_inicio+timedelta(minutes=self.DURACION_TURNO)
        return super().save(*args, **kwargs)
