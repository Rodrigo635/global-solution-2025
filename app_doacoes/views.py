from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Q
from app_contas.models import OngProfile
from app_contas.models import Categoria
from app_contas.models import CustomUser

def doacoes(request):
    user_signed = request.user
    
    ongs = OngProfile.objects.all()
    urgentes = OngProfile.objects.filter(emergencia=True)[:10]
    categorias = Categoria.objects.all()
    sugestoes = list(OngProfile.objects.filter(
        Q(user__categorias__in=user_signed.categorias.all()) |
        Q(user__cidade=user_signed.cidade)
    ).distinct()[:10])

    if len(sugestoes) < 10:
        faltando = 10 - len(sugestoes)
        outras = OngProfile.objects.exclude(pk__in=[ong.pk for ong in sugestoes]).order_by('?')[:faltando]
        sugestoes += list(outras)

    return render(request, 'doacoes.html', {'ongs': ongs, 'urgentes': urgentes,'sugestoes': sugestoes, 'categorias': categorias})


def explorar(request):
    ongs = OngProfile.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'explorar.html', {'ongs': ongs, 'categorias': categorias})

def ong(request, user):
    user_obj = get_object_or_404(CustomUser, username=user)
    ong = get_object_or_404(OngProfile, user=user_obj)
    return render(request, 'ong.html', {'ong': ong})