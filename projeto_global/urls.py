from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_global.urls')),
    path('rotas/', include(('app_rotas.urls', 'app_rotas'), namespace='rotas')),
    path('doacoes/', include(('app_doacoes.urls', 'app_doacoes'), namespace='doacoes')),
    path('alertas/', include(('app_alertas.urls', 'app_alertas'), namespace='alertas')),
    path('contas/', include(('app_contas.urls', 'app_contas'), namespace='contas')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
