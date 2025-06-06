# app_global/views.py

from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db.models import Q

from .models import Eventos, Pais, Estado, Cidade

def home(request):
    agora = timezone.now()

    # 1) Captura dos parâmetros de filtro via GET
    pais_sel   = request.GET.get('pais', '').strip()
    estado_sel = request.GET.get('estado', '').strip()
    cidade_sel = request.GET.get('cidade', '').strip()

    # 2) Querysets iniciais
    alertas_qs   = Eventos.objects.filter(Q(data_fim__gte=agora) | Q(data_fim__isnull=True))
    ocorridos_qs = Eventos.objects.filter(data_fim__lt=agora)

    # 3) Aplicar filtros de país / estado / cidade, se existirem
    if pais_sel:
        alertas_qs   = alertas_qs.filter(paises__nome__iexact=pais_sel)
        ocorridos_qs = ocorridos_qs.filter(paises__nome__iexact=pais_sel)

    if estado_sel:
        alertas_qs   = alertas_qs.filter(estados__nome__iexact=estado_sel)
        ocorridos_qs = ocorridos_qs.filter(estados__nome__iexact=estado_sel)

    if cidade_sel:
        alertas_qs   = alertas_qs.filter(cidades__nome__iexact=cidade_sel)
        ocorridos_qs = ocorridos_qs.filter(cidades__nome__iexact=cidade_sel)

    # 4) Remover duplicatas (due a joins ManyToMany) e ordenar
    alertas = alertas_qs.distinct().order_by('-data_inicio')
    ocorridos = ocorridos_qs.distinct().order_by('-data_fim')

    # 5) Listas para popular os <select> no template
    todos_paises  = Pais.objects.order_by('nome')
    todos_estados = Estado.objects.order_by('nome')
    todas_cidades = Cidade.objects.order_by('nome')

    context = {
        'alertas': alertas,
        'ocorridos': ocorridos,
        'paises': todos_paises,
        'estados': todos_estados,
        'cidades': todas_cidades,
        'pais_sel': pais_sel,
        'estado_sel': estado_sel,
        'cidade_sel': cidade_sel,
    }
    return render(request, 'home.html', context)


def eventos(request):
    agora = timezone.now()

    # 1) Captura dos parâmetros de busca e filtro vindos via GET
    busca      = request.GET.get('busca', '').strip()
    pais_sel   = request.GET.get('pais', '').strip()
    estado_sel = request.GET.get('estado', '').strip()
    cidade_sel = request.GET.get('cidade', '').strip()
    status_sel = request.GET.get('status', 'todos').strip()  # 'todos' | 'ativos' | 'ocorridos'

    # 2) Queryset inicial de todos os eventos
    qs = Eventos.objects.all()

    # 3) Filtrar por termo de busca (nome e descrição)
    if busca:
        qs = qs.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca))

    # 4) Filtrar por país
    if pais_sel:
        qs = qs.filter(paises__nome__iexact=pais_sel)

    # 5) Filtrar por estado
    if estado_sel:
        qs = qs.filter(estados__nome__iexact=estado_sel)

    # 6) Filtrar por cidade
    if cidade_sel:
        qs = qs.filter(cidades__nome__iexact=cidade_sel)

    # 7) Filtrar por status
    if status_sel == 'ativos':
        qs = qs.filter(Q(data_fim__gte=agora) | Q(data_fim__isnull=True))
    elif status_sel == 'ocorridos':
        qs = qs.filter(data_fim__lt=agora)
    # se status_sel == 'todos', não filtra nada

    # 8) Remover duplicatas e ordenar
    qs = qs.distinct().order_by('-data_inicio')

    # 9) Listas para popular selects
    todos_paises  = Pais.objects.order_by('nome')
    todos_estados = Estado.objects.order_by('nome')
    todas_cidades = Cidade.objects.order_by('nome')

    context = {
        'eventos': qs,
        'busca': busca,
        'pais_sel': pais_sel,
        'estado_sel': estado_sel,
        'cidade_sel': cidade_sel,
        'status_sel': status_sel,
        'paises': todos_paises,
        'estados': todos_estados,
        'cidades': todas_cidades,
    }
    return render(request, 'eventos.html', context)


def evento_detalhe(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    return render(request, 'evento_detalhe.html', {'evento': evento})
