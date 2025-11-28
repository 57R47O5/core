from django.db import models
from django.conf import settings

class AuditoriaLogin(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    username_intentado = models.CharField(max_length=150, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    exitoso = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username_intentado or self.usuario} - {'OK' if self.exitoso else 'FAIL'}"


class AuditoriaUsuario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="auditorias_realizadas"
    )
    usuario_afectado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="auditorias_recibidas"
    )
    accion = models.CharField(max_length=50)   # "CREAR", "EDITAR", "ELIMINAR"
    cambios = models.JSONField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} - {self.usuario_afectado}"
