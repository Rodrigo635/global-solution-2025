from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
# Vale lembrar que não sei django e o chatGPT tem total direito sobre o programa abaixo e é dever de conserta-lo. por fvaor não pedir para eu consertar. abraços
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class CustomUser(AbstractUser):
    # Campos comuns a todos
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True)
    cidade = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=(('pessoa', 'Pessoa'), ('ong', 'ONG')))


class OngProfile(models.Model):
    TIPO_CHAVE_PIX = [
        ('CPF/CNPJ', 'CPF/CNPJ'),
        ('Email', 'Email'),
        ('Telefone', 'Telefone'),
        ('Chave Aleatória', 'Chave Aleatória'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    cnpj = models.CharField(max_length=18)
    descricao = models.TextField()
    categorias = models.ManyToManyField('Categoria', blank=False)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    bairro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    site = models.URLField(blank=True, null=True)
    pix = models.CharField(max_length=50, blank=True, null=True)
    pixTipo = models.CharField(max_length=15, choices=TIPO_CHAVE_PIX, blank=True, null=True)
    emergencia = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
