from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Q
from app_contas.models import OngProfile
from app_contas.models import Categoria
from app_contas.models import CustomUser

def doacoes(request):
    user_signed = request.user
    sugestoes = []
    categorias = Categoria.objects.all()
    categoria_selecionada = request.GET.get('categoria', '')
    print(categoria_selecionada)

    if categoria_selecionada and categoria_selecionada != 'todas':
        ongs = OngProfile.objects.filter(user__categorias__nome=categoria_selecionada).distinct()[:10]
    else:
        ongs = OngProfile.objects.all()[:10]

    urgentes = OngProfile.objects.filter(emergencia=True)[:10]

    if user_signed.is_authenticated:
        sugestoes = list(OngProfile.objects.filter(
            Q(user__categorias__in=user_signed.categorias.all()) |
            Q(user__cidade=user_signed.cidade)
        ).distinct()[:10])
    if not sugestoes or len(sugestoes) < 10:
        faltando = 10 - len(sugestoes)
        outras = OngProfile.objects.exclude(pk__in=[ong.pk for ong in sugestoes]).order_by('?')[:faltando]
        sugestoes += list(outras)

    # Se for uma requisição AJAX, renderiza só os cards
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/card_explorar.html', {'ongs': ongs}, request=request)
        return JsonResponse({'html': html})

    context = {
        'ongs': ongs,
        'urgentes': urgentes,
        'sugestoes': sugestoes,
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,
    }
    return render(request, 'doacoes.html', context)



def explorar(request):
    query = request.GET.get('busca', '').strip()
    categoria_filtro = request.GET.get('categoria', '')

    # IMPORTANTE: Adicionar ordenação para evitar warnings
    ongs = OngProfile.objects.all().order_by('user')  # Mais recentes primeiro

    if query:
        ongs = ongs.filter(
            Q(user__username__icontains=query) |
            Q(descricao__icontains=query) |
            Q(user__categorias__nome__icontains=query) |
            Q(user__cidade__icontains=query)
        )

    if categoria_filtro and categoria_filtro != 'todas':
        ongs = ongs.filter(user__categorias__nome__icontains=categoria_filtro)

    ongs = ongs.distinct()

    # Paginação
    page_number = request.GET.get('page', 1)
    paginator = Paginator(ongs, 3)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/explorar/card.html', {'ongs': page_obj}, request=request)
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    categorias = Categoria.objects.all()
    return render(request, 'explorar.html', {
        'ongs': page_obj,
        'categorias': categorias,
        'query': query,
        'categoria_selecionada': categoria_filtro
    })

def ong(request, user):
    user_obj = get_object_or_404(CustomUser, username=user)
    ong = get_object_or_404(OngProfile, user=user_obj)
    imagesOng = ong.gallery_images.all()
    return render(request, 'ong.html', {'ong': ong, 'fotos': imagesOng})