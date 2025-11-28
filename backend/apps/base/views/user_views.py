from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_protect

from apps.base.framework.api.options import BaseOptionsAPIView
from apps.carteles.permisos import EsMedico
from apps.base.models.user import User
from apps.base.serializers import UserCreateSerializer, UserUpdateSerializer, UserRegisterSerializer
from apps.base.framework.exceptions import excepcion, ExcepcionValidacion

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

@excepcion
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, EsMedico])
def usuario_retrieve_update(request, pk):
    try:
        usuario = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"mensaje": "Usuario no encontrado"}, status=404)

    if request.method == 'GET':
        serializer = UserUpdateSerializer(usuario)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(usuario, data=request.data, partial=True)
        if not serializer.is_valid():
            raise ExcepcionValidacion(f'{serializer.errors}')
        serializer.save()
        return Response(serializer.data)
    
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

class UserRolesOptions(BaseOptionsAPIView):
    model=User
    field='rol'