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
                    return redirect(request.GET.get('next', 'home'))
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
            auth_login(request, user)
            return redirect('home')
        
    else:
        form = DoadorRegistrationForm()
    
    return render(request, 'registerDonor.html', {'form': form})

def registerOng(request):
    if request.method == 'POST':
        form = OngRegistrationForm(request.POST, request.FILES)
        
        # Validação manual das imagens antes de processar o form
        gallery_images = request.FILES.getlist('gallery_images')
        image_errors = []
        
        if len(gallery_images) > 6:
            image_errors.append("Máximo de 6 imagens permitidas.")
        
        for img in gallery_images:
            if img.size > 5 * 1024 * 1024:
                image_errors.append(f"A imagem '{img.name}' excede o tamanho máximo de 5MB.")
            
            if not img.content_type.startswith('image/'):
                image_errors.append(f"O arquivo '{img.name}' não é uma imagem válida.")
        
        # Se há erros nas imagens, adicione ao form
        if image_errors:
            for error in image_errors:
                form.add_error('gallery_images', error)
        
        if form.is_valid() and not image_errors:
            try:
                with transaction.atomic():
                    # Salvar usuário
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.tipo = form.cleaned_data.get('tipo')
                    user.save()
                    user.categorias.set(form.cleaned_data['categorias'])
                    
                    # Salvar perfil da ONG
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
                    
                    # Salvar imagens da galeria
                    for img in gallery_images:
                        if img:
                            obj= GalleryImage.objects.create(
                                image=img,
                                ong=ong
                            )
                            ong.gallery_images.add(obj)
                    
                    auth_login(request, user)
                    return redirect('home')
                    
            except Exception as e:
                print(f"Erro detalhado: {e}")
        else:
            print("Erros do form:", form.errors)
            if image_errors:
                print("Erros das imagens:", image_errors)
    else:
        form = OngRegistrationForm()
    
    return render(request, 'registerOng.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')
    