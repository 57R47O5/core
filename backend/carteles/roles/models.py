from django.db import models
from apps.base.models.user import User

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')
