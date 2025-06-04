from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('evento/<int:evento_id>/', evento_detalhe, name='evento_detalhe'),
    path('eventos/', eventos, name='eventos'),
]