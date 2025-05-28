from django.urls import path
from .views import *

app_name = 'rotas'

urlpatterns = [
    path('', rotas, name='rotas'),
]
