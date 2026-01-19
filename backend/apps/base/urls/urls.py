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
    path("", include("apps.base.rest_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
