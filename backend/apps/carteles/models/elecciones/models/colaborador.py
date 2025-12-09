from django.db import models
from .campana import Campana
from apps.base.models.user import User

class Colaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, db_index=True)
    role = models.CharField(max_length=50, default="militante")
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['campana']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.campaign}"