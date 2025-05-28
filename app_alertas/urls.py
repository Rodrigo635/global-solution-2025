from django.urls import path
from .views import *

app_name = 'alertas'

urlpatterns = [
    path('', alertas, name='alertas'),
]