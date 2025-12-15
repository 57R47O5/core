from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.base.framework.exceptions import excepcion, ExcepcionPermisos, ExcepcionValidacion
from apps.base.framework.permissions import get_roles

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
            'username': user.nombres,
            'email': user.email,
            "roles": list(get_roles(user)),
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
    if not request.user.is_authenticated:
        return Response({"isAuthenticated": False})

    return Response({
        "isAuthenticated": True,
        "user": {
            "id": request.user.id,
            "username": request.user.nombres,
            "roles": list(get_roles(request.user)),
        }
    })

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

