from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('autenticacao.urls')),    
    path('', include('cursos.urls')),    
    path('eventos/', include('eventos.urls')),    
    path('servicos/', include('cevest_os.urls')),
    path('almoxarifado/', include('cevest_almoxarifado.urls')),    
    path('newsletter/', include('newsletter.urls')),

    path('administracao/', include('administracao.urls')),    
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
