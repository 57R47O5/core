from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.base.serializers import UserLookupSerializer
from apps.base.framework.exceptions import excepcion, ExcepcionPermisos, ExcepcionValidacion
from apps.base.models.user import User
from apps.base.serializers import UserSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
@excepcion
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        raise ExcepcionValidacion('Debe ingresar usuario y contraseña')

    user = authenticate(request, username=username, password=password)

    if user is None:
        raise ExcepcionPermisos('Credenciales inválidas')
    login(request, user)
    datos_usuario={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'rol': user.rol or None,
        }
    return Response({
        'message': 'Inicio de sesión exitoso.',
        'user': datos_usuario
    }, status=status.HTTP_200_OK)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_protect
def logout_view(request):
    logout(request)
    return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)

@api_view(["GET"])
def check_auth(request):
    is_authenticated = request.user.is_authenticated
    user_data=None
    if is_authenticated:
        usuario=User.objects.get(pk=request.user.id)
        serializer = UserSerializer(instance=usuario)
        user_data =  serializer.data

    return Response(
        {"isAuthenticated": is_authenticated, "user": user_data},
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
def password_reset_request(request):
    if request.method == "POST":
        serializer = UserLookupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        subject = "Solicitud de cambio de contraseña"
        email_template_name = "registration/password_reset_email.html"
        c = {
            "email": user.email,
            "domain": settings.DOMAIN_NAME,
            "site_name": settings.SITE_NAME,
            "uid": uid,
            "user": user,
            "token": token,
            "protocol": "http",
        }
        email_content = render_to_string(email_template_name, c)
        send_mail(
            subject,
            email_content,
            settings.EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Password reset email has been sent"}, status=status.HTTP_200_OK
        )


@api_view(["POST"])
def password_reset_confirm(request, uidb64, token):
    """
    Vista para confirmar el reseteo de contraseña y establecer una nueva.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        return Response(
            {"error": "UID inválido."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Buscar el usuario usando el serializer
    serializer = UserLookupSerializer(data={"pk": uid})
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()

    if user is not None and default_token_generator.check_token(user, token):
        new_password = request.data.get("password")
        if not new_password:
            return Response(
                {"error": "Se necesita una nueva contraseña."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "La contraseña ha sido cambiada exitosamente."},
            status=status.HTTP_200_OK,
        )

    return Response(
        {"error": "El token es inválido o ha expirado."},
        status=status.HTTP_400_BAD_REQUEST,
    )

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

