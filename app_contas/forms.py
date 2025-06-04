# forms.py
from django import forms

from app_global.models import *
from .models import *
from django.contrib.auth import get_user_model
from multiupload.fields import MultiFileField

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class DoadorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all().order_by("nome"),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_pais"}),
        required=True,
        empty_label="Selecione um país",
    )
    
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_estado"}),
        required=True,
        empty_label="Selecione um estado",
    )
    
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_cidade"}),
        required=True,
        empty_label="Selecione uma cidade",
    )
    
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
    
    imagem = forms.ImageField(
        required=True, 
        help_text="Formatos aceitos: JPG, PNG. Tamanho máximo: 5MB"
    )

    class Meta:
        model = CustomUser  # Assumindo que você está usando CustomUser
        fields = ["username", "email", "password", "cidade", "imagem", "categorias"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se há dados POST (durante validação)
        if 'pais' in self.data:
            try:
                pais_id = int(self.data.get('pais'))
                self.fields['estado'].queryset = Estado.objects.filter(
                    pais_id=pais_id
                ).order_by('nome')
            except (ValueError, TypeError):
                pass  # Valor inválido, mantém queryset vazio
        
        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Cidade.objects.filter(
                    estado_id=estado_id
                ).order_by('nome')
            except (ValueError, TypeError):
                pass  # Valor inválido, mantém queryset vazio
        
        # Para edição (se a instância já existe)
        elif self.instance.pk and hasattr(self.instance, 'cidade') and self.instance.cidade:
            # Carrega estado e cidade da instância existente
            self.fields['estado'].queryset = Estado.objects.filter(
                pais=self.instance.cidade.estado.pais
            ).order_by('nome')
            self.fields['cidade'].queryset = Cidade.objects.filter(
                estado=self.instance.cidade.estado
            ).order_by('nome')

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        pais = self.cleaned_data.get('pais')
        
        if estado and pais:
            # Verifica se o estado pertence ao país selecionado
            if not Estado.objects.filter(id=estado.id, pais=pais).exists():
                raise forms.ValidationError("Estado inválido para o país selecionado.")
        
        return estado

    def clean_cidade(self):
        cidade = self.cleaned_data.get('cidade')
        estado = self.cleaned_data.get('estado')
        
        if cidade and estado:
            # Verifica se a cidade pertence ao estado selecionado
            if not Cidade.objects.filter(id=cidade.id, estado=estado).exists():
                raise forms.ValidationError("Cidade inválida para o estado selecionado.")
        
        return cidade

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "As senhas não coincidem")
        
        # Define o tipo como pessoa
        cleaned_data["tipo"] = "pessoa"
        
        print(cleaned_data)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.tipo = "pessoa"
        
        if commit:
            user.save()
            # Salva as categorias (ManyToMany)
            self.save_m2m()
        
        return user

class OngRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    # Campos específicos para ONGs
    cnpj = forms.CharField(max_length=18, label="CNPJ")
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}), 
        label="Descrição da ONG"
    )
    telefone = forms.CharField(max_length=20)
    rua = forms.CharField(max_length=200)
    cep = forms.CharField(max_length=8)
    bairro = forms.CharField(max_length=100)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=100, required=False)
    site = forms.URLField(required=False)
    
    gallery_images = MultiFileField(
        min_num=0,
        max_num=6,
        max_file_size=1024 * 1024 * 5,  # 5MB
        required=False,
        label="Galeria de Fotos (Máx. 6)",
        help_text="Selecione até 6 imagens para a galeria. Formatos aceitos: JPG, PNG. Tamanho máximo por imagem: 5MB",
    )
    
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
    
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all().order_by("nome"),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_pais"}),
        required=True,
        empty_label="Selecione um país",
    )
    
    estado= forms.ModelChoiceField(  # Renomeado para evitar conflito
        queryset=Estado.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_estado"}),
        required=True,
        empty_label="Selecione um estado",
    )
    
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_cidade"}),
        required=True,
        empty_label="Selecione uma cidade",
    )
    
    pix = forms.CharField(max_length=100, required=False, label="Chave PIX")
    pixTipo = forms.ChoiceField(
        choices=OngProfile.TIPO_CHAVE_PIX,
        required=False,
        label="Tipo de Chave PIX",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    
    imagem = forms.ImageField(
        required=True,
        label="Logo/Marca da ONG",
        help_text="Formatos aceitos: JPG, PNG. Tamanho máximo: 5MB",
    )

    class Meta:
        model = CustomUser  # Assumindo CustomUser
        fields = ["username", "email", "password", "cidade", "imagem", "categorias"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se há dados POST (durante validação)
        if 'pais' in self.data:
            try:
                pais_id = int(self.data.get('pais'))
                self.fields['estado'].queryset = Estado.objects.filter(
                    pais_id=pais_id
                ).order_by('nome')
            except (ValueError, TypeError):
                pass  # Valor inválido, mantém queryset vazio
        
        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Cidade.objects.filter(
                    estado_id=estado_id
                ).order_by('nome')
            except (ValueError, TypeError):
                pass  # Valor inválido, mantém queryset vazio
        
        # Para edição (se a instância já existe)
        elif self.instance.pk and hasattr(self.instance, 'cidade') and self.instance.cidade:
            # Carrega estado e cidade da instância existente
            self.fields['estado'].queryset = Estado.objects.filter(
                pais=self.instance.cidade.estado.pais
            ).order_by('nome')
            self.fields['cidade'].queryset = Cidade.objects.filter(
                estado=self.instance.cidade.estado
            ).order_by('nome')

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        pais = self.cleaned_data.get('pais')
        
        if estado and pais:
            # Verifica se o estado pertence ao país selecionado
            if not Estado.objects.filter(id=estado.id, pais=pais).exists():
                raise forms.ValidationError("Estado inválido para o país selecionado.")
        
        return estado

    def clean_cidade(self):
        cidade = self.cleaned_data.get('cidade')
        estado = self.cleaned_data.get('estado')
        
        if cidade and estado:
            # Verifica se a cidade pertence ao estado selecionado
            if not Cidade.objects.filter(id=cidade.id, estado=estado).exists():
                raise forms.ValidationError("Cidade inválida para o estado selecionado.")
        
        return cidade

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Remove caracteres não numéricos
            cnpj_numbers = ''.join(filter(str.isdigit, cnpj))
            
            # Validação básica de CNPJ (14 dígitos)
            if len(cnpj_numbers) != 14:
                raise forms.ValidationError("CNPJ deve ter 14 dígitos.")
            
            # Aqui você pode adicionar validação mais completa do CNPJ
            # Por enquanto, retorna formatado
            return cnpj_numbers
        
        return cnpj

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove caracteres não numéricos
            cep_numbers = ''.join(filter(str.isdigit, cep))
            
            if len(cep_numbers) != 8:
                raise forms.ValidationError("CEP deve ter 8 dígitos.")
            
            return cep_numbers
        
        return cep

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "As senhas não coincidem")
        
        # Define o tipo como ong
        cleaned_data["tipo"] = "ong"
        
        # Validação PIX
        pix = cleaned_data.get("pix")
        pix_tipo = cleaned_data.get("pixTipo")
        
        if pix and not pix_tipo:
            self.add_error("pixTipo", "Selecione o tipo da chave PIX.")
        elif pix_tipo and not pix:
            self.add_error("pix", "Informe a chave PIX.")
        
        print(cleaned_data)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.tipo = "ong"
        
        if commit:
            user.save()
            
            # Criar ou atualizar perfil da ONG
            ong_profile, created = OngProfile.objects.get_or_create(
                user=user,
                defaults={
                    'cnpj': self.cleaned_data.get('cnpj'),
                    'descricao': self.cleaned_data.get('descricao'),
                    'telefone': self.cleaned_data.get('telefone'),
                    'rua': self.cleaned_data.get('rua'),
                    'cep': self.cleaned_data.get('cep'),
                    'bairro': self.cleaned_data.get('bairro'),
                    'numero': self.cleaned_data.get('numero'),
                    'complemento': self.cleaned_data.get('complemento'),
                    'site': self.cleaned_data.get('site'),
                    'pix': self.cleaned_data.get('pix'),
                    'pixTipo': self.cleaned_data.get('pixTipo'),
                }
            )
            
            # Salva as categorias (ManyToMany)
            self.save_m2m()
            
            # Processa imagens da galeria se houver
            gallery_images = self.cleaned_data.get('gallery_images', [])
            for image in gallery_images:
                # Aqui você salvaria as imagens da galeria
                # Isso depende de como você estruturou o modelo de galeria
                pass
        
        return user
