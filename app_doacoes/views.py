from django.shortcuts import render
from django.shortcuts import get_object_or_404
from app_contas.models import OngProfile
from app_contas.models import Categoria
from app_contas.models import CustomUser

def doacoes(request):
    ongs = OngProfile.objects.all()
    categorias = Categoria.objects.all()

    urgentes = OngProfile.objects.filter(emergencia=True)[:10]

    return render(request, 'doacoes.html', {'ongs': ongs, 'categorias': categorias, 'urgentes': urgentes})


def explorar(request):
    ongs = OngProfile.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'explorar.html', {'ongs': ongs, 'categorias': categorias})

def ong(request, user):
    user_obj = get_object_or_404(CustomUser, username=user)
    ong = get_object_or_404(OngProfile, user=user_obj)
    return render(request, 'ong.html', {'ong': ong})