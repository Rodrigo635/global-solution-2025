from django.urls import path
from .views import *

app_name = 'contas'

urlpatterns = [
    path('', contas, name='contas'),
]