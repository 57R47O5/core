from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.base.views.views import (get_csrf_token, 
                    check_auth, login_view, logout_view, 
                  )

urlpatterns = [
    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('csrf/', get_csrf_token, name='get-csrf-token'),
    path('check-auth/', check_auth, name='check_auth'),
    path('usuarios/', include('apps.base.urls.user_urls')), 
    path('carteles/', include('apps.carteles.urls.carteles_urls')), 
    path('personas/', include('apps.carteles.urls.personas_urls')), 
    path('pacientes/', include('apps.carteles.urls.paciente_urls')), 
    path('turnos/', include('apps.carteles.urls.turno_urls')), 
    path('tipo-carteles/', include('apps.carteles.urls.tipo_cartel_urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
