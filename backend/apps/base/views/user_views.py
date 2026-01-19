from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_protect

from apps.base.framework.api.options import BaseOptionsAPIView
from apps.carteles.permisos import EsMedico
from apps.base.models.user import User
from apps.base.serializers.user_serializer import UserCreateSerializer, UserRegisterSerializer, UsuarioUpdateSerializer
from apps.base.framework.exceptions import excepcion, ExcepcionValidacion
from apps.base.framework.permissions import get_roles

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, EsMedico])   
def usuarios_list_create(request):
    if request.method == 'GET':
        usuarios = User.objects.all().order_by('username')
        serializer = UserCreateSerializer(usuarios, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
@excepcion
def register_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        raise ExcepcionValidacion(f'Error en el registro: {serializer.errors}')
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class MedicosOptions(BaseOptionsAPIView):
    model=User
    filtro={'role':'medico'}

@api_view(['GET'])
def roles_view(request, pk):
    roles = get_roles(User.objects.get(pk=pk))
    return Response(list(roles), status=status.HTTP_200_OK)

@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def usuario_detail(request, pk):
    """
    Ver un usuario o actualizarlo.
    """

    try:
        usuario = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UsuarioUpdateSerializer(usuario)
        return Response(serializer.data)

    # PUT o PATCH → actualización
    partial = request.method == "PATCH"
    serializer = UsuarioUpdateSerializer(usuario, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)