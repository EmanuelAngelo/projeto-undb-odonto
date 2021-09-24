from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from core import settings


urlpatterns = [
    
    path('', include('base.urls')),
    path('admin/', admin.site.urls),
    path('box/', include('box.urls')),
    path('user/', include('user.urls')),
    path('logout/', LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),  name='logout'),
]

from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
