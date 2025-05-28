from django.urls import path
from .views import *

urlpatterns = [
    # Home
    path('', home, name='home'),
    path('inicio/', inicio, name='inicio'),

    # Autenticacao
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]