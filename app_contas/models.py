from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from app_global.models import Cidade

# Create your models here.
# Vale lembrar que não sei django e o chatGPT tem total direito sobre o programa abaixo e é dever de conserta-lo. por fvaor não pedir para eu consertar. abraços

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class CustomUnicodeUsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w\s.@+-]+$'  # Adicionado \s para permitir espaços
    message = 'Digite um nome válido. Este valor pode conter apenas letras, números, espaços e os caracteres @/./+/-/_.'


class CustomUser(AbstractUser):
    # Sobrescrever o campo username com validador customizado
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[CustomUnicodeUsernameValidator()],
        error_messages={
            'unique': "Já existe um usuário com este nome.",
        },
        verbose_name='Nome de usuário'
    )
    
    # Campos comuns a todos
    categorias = models.ManyToManyField('Categoria', blank=False)
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True)
    
    # Apenas cidade - estado e país são acessados via cidade.estado e cidade.estado.pais
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    
    tipo = models.CharField(
        max_length=10,
        choices=(('pessoa', 'Pessoa'), ('ong', 'ONG'))
    )
    
    @property
    def estado(self):
        return self.cidade.estado
    
    @property
    def pais(self):
        return self.cidade.estado.pais
    
    def __str__(self):
        return self.username

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='ong_gallery/')
    ong = models.ForeignKey('OngProfile', related_name='gallery_images', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']


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
    telefone = models.CharField(max_length=20)
    rua = models.CharField(max_length=200)
    cep = models.CharField(max_length=8)
    bairro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    site = models.URLField(blank=True, null=True)
    pix = models.CharField(max_length=50, blank=True, null=True)
    pixTipo = models.CharField(max_length=15, choices=TIPO_CHAVE_PIX, blank=True, null=True)
    emergencia = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ONG: {self.user.username}"
    
    @property
    def gallery_count(self):
        """Retorna o número de imagens na galeria"""
        return self.gallery_images.count()
    
    def get_featured_image(self):
        """Retorna a primeira imagem da galeria como imagem destacada"""
        return self.gallery_images.first()