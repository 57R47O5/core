from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import register_view, get_csrf_token, check_auth, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('csrf/', get_csrf_token, name='get-csrf-token'),
    path('check-auth/', check_auth, name='check_auth'),
    path('carteles/', include('apps.carteles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
