from django.shortcuts import render

def doacoes(request):
    return render(request, 'doacoes.html')

def explorar(request):
    return render(request, 'explorar.html')	
