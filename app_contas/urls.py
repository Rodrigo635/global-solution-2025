from django.conf.urls.static import static
from django.urls import path

from projeto_global import settings
from .views import *

app_name = 'contas'

urlpatterns = [
    path('', contas, name='contas'),

    # Autenticacao
    path('register/', register, name='register'),
    path('register/ong', registerOng, name='registerOng'),
    path('register/donor', registerDonor, name='registerDonor'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('carregar-cidades/', carregar_cidades, name='carregar_cidades'),
    path('carregar-estados/', carregar_estados, name='carregar_estados'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)