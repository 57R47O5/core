from apps.elecciones.urls.campana_urls import urlpatterns as campana_urls
from apps.elecciones.urls.colaborador_urls import urlpatterns as colaborador_urls
from apps.elecciones.urls.ciclo_electoral_urls import  urlpatterns  as ciclo_electoral_urls
from apps.elecciones.urls.estado_salida_urls import urlpatterns as estado_salida_urls
from apps.elecciones.urls.resultado_visita_urls import urlpatterns as resultado_visita_urls
from apps.elecciones.urls.salida_urls import urlpatterns as salida_urls
from apps.elecciones.urls.seccional_urls import urlpatterns as seccional_urls
from apps.elecciones.urls.votante_urls import urlpatterns as votante_urls

urlpatterns = (
    campana_urls
    + colaborador_urls
    + ciclo_electoral_urls
    + estado_salida_urls
    + resultado_visita_urls
    + salida_urls
    + seccional_urls
    + votante_urls
)
