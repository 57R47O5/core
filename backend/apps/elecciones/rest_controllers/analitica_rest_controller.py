from rest_framework.response import Response
from rest_framework import status, viewsets
from controllers.base.base_rest_controller import BaseRestController
from apps.elecciones.services.analitica_electoral_service import AnaliticaElectoralService

class AnaliticaRestController(viewsets.ViewSet):

    def list(self, request):
        datos_analitica = AnaliticaElectoralService.obtener_datos_analitica()
        return Response(datos_analitica, status=status.HTTP_200_OK)