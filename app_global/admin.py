from django.contrib import admin
from .models import Pessoa, Animal

# Register your models here.
admin.site.register(Pessoa)
admin.site.register(Animal)