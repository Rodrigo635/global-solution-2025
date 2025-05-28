from django.shortcuts import render

def rotas(request):
    return render(request, 'rotas.html')