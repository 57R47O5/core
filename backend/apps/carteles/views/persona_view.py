from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from ..models.persona import Persona
from ..serializers.persona_serializer import PersonaSerializer
from apps.base.framework.exceptions import excepcion


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
@excepcion
def persona_list_create(request):
    """
    GET: Lista todas las personas (solo admin).
    POST: Crea una persona asociada al usuario autenticado.
    """
    user = request.user

    if request.method == "GET":
        personas = Persona.objects.all().values("id", "nombre")
        return Response(personas, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if hasattr(user, "persona"):
            return Response(
                {"detail": "Este usuario ya tiene una persona asociada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        datos = request.data.copy()
        datos["usuario"] = user.id

        serializer = PersonaSerializer(data=datos)
        serializer.is_valid(raise_exception=True)
        persona = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
@excepcion
def persona_detail(request, pk):
    """
    GET: Obtiene una persona por ID.
    PUT: Actualiza la persona.
    DELETE: Elimina la persona.
    """
    try:
        persona = Persona.objects.get(pk=pk)
    except Persona.DoesNotExist:
        return Response(
            {"detail": "Persona no encontrada."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = PersonaSerializer(persona)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = PersonaSerializer(persona, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        persona.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
