from django.shortcuts import render

def doacoes(request):
    return render(request, 'doacoes.html')