from django.shortcuts import render

def contas(request):
    return render(request, 'contas.html')