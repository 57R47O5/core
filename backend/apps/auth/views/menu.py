from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from framework.menu.menu_service import get_menu_for

@api_view(["GET"])
def menu_view(request):
    menu = get_menu_for(request.user)
    return Response(menu)