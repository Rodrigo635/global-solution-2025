from django.urls import path
from .views import *

urlpatterns = [
    # Home
    path('', home, name='home'),
]