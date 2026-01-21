from django.db import models

class User(models.Model):
    """
    Identidad técnica del sistema.
    No representa una persona.
    """

    # Identidad de login
    email = models.EmailField(unique=True)

    # Seguridad
    password_hash = models.CharField(max_length=255)

    # Estado
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False)

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return self.email
