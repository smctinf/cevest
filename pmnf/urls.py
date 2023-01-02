from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from pmnf import settings

admin.site.site_header = "CEVEST - Prefeitura Municipal de Nova Friburgo"
admin.site.site_title = "CEVEST"

urlpatterns = [
    path('', include('cevest.urls')),
    path('administracao/', include('Administracao.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

# Include the media URL patterns only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
