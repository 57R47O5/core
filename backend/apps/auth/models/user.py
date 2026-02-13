from django.db import models

class User(models.Model):
    """
    Identidad técnica del sistema.
    No representa una persona.
    """

    # Identidad lógica
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Identificador lógico estable del usuario"
    )

    # Identidad de contacto
    email = models.EmailField(
        unique=True,
        help_text="Email de contacto (no identidad primaria)"
    )

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
    
    @property
    def roles(self):
        roles = []
        for user_rol in self.user_roles.all():
            roles.append(user_rol.rol.nombre)
        return roles
    
    def is_owner(self):
        return "Owner" in self.roles
    
    @property
    def permisos(self):
        from django.apps import apps
        # Caso especial técnico
        if self.is_owner():
            Permiso = apps.get_model("auth", "Permiso")
            return Permiso.objects.values_list("codigo", flat=True)

        return self.user_roles.values_list(
            "rol__permisos__permiso",
            flat=True
        )
