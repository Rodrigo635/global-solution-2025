# forms.py
from django import forms
from .models import Categoria
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class DoadorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'cidade']

    def clean(self):
        cleaned_data = super().clean()
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
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'cidade']

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data
    