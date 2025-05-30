from django.urls import path
from .views import *

app_name = 'doacoes'

urlpatterns = [
    path('', doacoes, name='doacoes'),
    path('explorar/', explorar, name='explorar'),
]