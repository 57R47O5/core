from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    dni = models.CharField(max_length=15, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})" if self.dni else self.nombre
