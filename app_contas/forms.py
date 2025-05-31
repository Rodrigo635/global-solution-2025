# forms.py
from django import forms
from .models import Categoria, OngProfile
from django.contrib.auth import get_user_model
from multiupload.fields import MultiFileField

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class DoadorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )

    imagem = forms.ImageField(
        required=True,
        help_text='Formatos aceitos: JPG, PNG. Tamanho máximo: 5MB'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'cidade', 'imagem', 'categorias']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('password', "As senhas não coincidem")

        cleaned_data['tipo'] = 'pessoa'
        print(cleaned_data)
        return cleaned_data
    
class OngRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    # Campos específicos para ONGs
    cnpj = forms.CharField(max_length=18, label='CNPJ')
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Descrição da ONG')
    telefone = forms.CharField(max_length=20)
    endereco = forms.CharField(max_length=200)
    estado = forms.CharField(max_length=2)
    cep = forms.CharField(max_length=8)
    bairro = forms.CharField(max_length=100)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=100, required=False)
    site = forms.URLField(required=False)

    gallery_images = MultiFileField(
        min_num=0,
        max_num=6,
        max_file_size=1024*1024*5,  # 5MB
        required=False,
        label='Galeria de Fotos (Máx. 6)',
        help_text='Selecione até 6 imagens para a galeria. Formatos aceitos: JPG, PNG. Tamanho máximo por imagem: 5MB'
    )

    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )
    

    pix = forms.CharField(
        max_length=100,
        required=False,
        label='Chave PIX'
    )

    pixTipo = forms.ChoiceField(
        choices=OngProfile.TIPO_CHAVE_PIX,
        required=False,
        label='Tipo de Chave PIX',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    imagem = forms.ImageField(
        required=True,
        label='Logo/Marca da ONG',
        help_text='Formatos aceitos: JPG, PNG. Tamanho máximo: 5MB'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'cidade', 'imagem', 'categorias']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('password', "As senhas não coincidem")

        cleaned_data['tipo'] = 'ong'
        print(cleaned_data)
        return cleaned_data
    