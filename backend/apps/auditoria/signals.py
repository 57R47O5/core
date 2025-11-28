from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import AuditoriaLogin, AuditoriaUsuario
from apps.base.models.user import User

def get_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0]
    return request.META.get("REMOTE_ADDR")

@receiver(user_logged_in)
def login_exitoso(sender, request, user, **kwargs):
    AuditoriaLogin.objects.create(
        usuario=user,
        username_intentado=user.username,
        exitoso=True,
        ip=get_ip(request),
    )

@receiver(user_login_failed)
def login_fallido(sender, credentials, request, **kwargs):
    AuditoriaLogin.objects.create(
        username_intentado=credentials.get("username"),
        exitoso=False,
        ip=get_ip(request) if request else None,
    )

@receiver(post_save, sender=User)
def auditar_usuario_guardado(sender, instance, created, **kwargs):
    request = getattr(instance, "_request", None)

    if not request:
        return  # evita auditoría sin contexto

    usuario_actor = request.user if request.user.is_authenticated else None

    if created:
        AuditoriaUsuario.objects.create(
            usuario=usuario_actor,
            usuario_afectado=instance,
            accion="CREAR",
            cambios=None
        )
    else:
        # capturar campos cambiados
        if hasattr(instance, "_original_state"):
            cambios = {}
            for campo, valor_original in instance._original_state.items():
                valor_nuevo = getattr(instance, campo)
                if valor_original != valor_nuevo:
                    cambios[campo] = {
                        "antes": valor_original,
                        "después": valor_nuevo
                    }

            if cambios:
                AuditoriaUsuario.objects.create(
                    usuario=usuario_actor,
                    usuario_afectado=instance,
                    accion="EDITAR",
                    cambios=cambios
                )


@receiver(pre_delete, sender=User)
def auditar_usuario_eliminado(sender, instance, **kwargs):
    request = getattr(instance, "_request", None)
    usuario_actor = request.user if request and request.user.is_authenticated else None

    AuditoriaUsuario.objects.create(
        usuario=usuario_actor,
        usuario_afectado=instance,
        accion="ELIMINAR",
        cambios=None
    )