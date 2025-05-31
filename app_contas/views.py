from django.db import transaction
from django.shortcuts import render
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from .models import *

def contas(request):
    return render(request, 'contas.html')

def register(request):
    return render(request, 'registerSelector.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                username = User.objects.get(email=email).username
                user = authenticate(
                    request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect(request.GET.get('next', 'inicio'))
                else:
                    form.add_error(None, 'Email ou senha incorretos')
            except User.DoesNotExist:
                form.add_error('email', 'Email não registrado')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registerDonor(request):
    print("Entrou no registerDonor")
    if request.method == 'POST':
        form = DoadorRegistrationForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.tipo = form.cleaned_data.get('tipo')
            user.save()
            user.categorias.set(form.cleaned_data['categorias'])
            user.save()
            auth_login(request, user)
            return redirect('inicio')
        
    else:
        form = DoadorRegistrationForm()
    
    return render(request, 'registerDonor.html', {'form': form})

def registerOng(request):
    if request.method == 'POST':
        form = OngRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.tipo = form.cleaned_data.get('tipo')
                    user.save()
                    user.categorias.set(form.cleaned_data['categorias'])
                    user.save()

                    ong = OngProfile.objects.create(
                        user=user,
                        cnpj=form.cleaned_data['cnpj'],
                        descricao=form.cleaned_data['descricao'],
                        telefone=form.cleaned_data['telefone'],
                        endereco=form.cleaned_data['endereco'],
                        estado=form.cleaned_data['estado'],
                        cep=form.cleaned_data['cep'],
                        bairro=form.cleaned_data['bairro'],
                        numero=form.cleaned_data['numero'],
                        complemento=form.cleaned_data.get('complemento', ''),
                        pix=form.cleaned_data.get('pix'),
                        pixTipo=form.cleaned_data.get('pixTipo'),
                        site=form.cleaned_data.get('site')
                    )
                    auth_login(request, user)
                    return redirect('inicio')

            except Exception as e:
                form.add_error(None, f"Ocorreu um erro ao salvar a ONG: {e}")
        else:
            print(form.errors)

    else:
        form = OngRegistrationForm()

    return render(request, 'registerOng.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')
    