
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from framework.permisos import P, require_perm
from apps.auth.permisos import AuthPermisos
from apps.auth.services.user_service import User, UserService

class RegisterView(APIView):

    @require_perm(P(AuthPermisos.REGISTER))
    def post(self, request):
        data = request.data or {}

        user = UserService.create_user(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
        )

        return Response(
            {
                "id": user.pk,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserListView(APIView):
    """
    Lista los usuarios del sistema.
    """

    def get(self, request):

        queryset = User.objects.all().order_by("username")

        serializer = UserListSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)