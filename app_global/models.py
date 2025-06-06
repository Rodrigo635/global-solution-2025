# models.py
from django.db import models
from django.utils import timezone

class Pais(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Estado(models.Model):
    nome = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Eventos(models.Model):
    TIPO_CHOICES = (
        ('chuva_forte', 'Chuva Forte'),
        ('tempestade', 'Tempestade'),
        ('enchente', 'Enchente'),
        ('geada', 'Geada'),
        ('granizo', 'Granizo'),
        ('nevasca', 'Nevasca'),

        ('furacao', 'Furacão'),
        ('tornado', 'Tornado'),
        ('vendaval', 'Vendaval'),
        
        ('seca', 'Seca'),
        ('incendio', 'Incêndio Florestal'),
        ('queimada', 'Queimada'),

        ('deslizamento', 'Deslizamento de Terra'),
        ('terremoto', 'Terremoto'),
        ('tremor', 'Tremor de Terra'),
        ('tsunami', 'Tsunami'),

        ('atividade_volcanica', 'Atividade Vulcânica'),
        ('erupcao', 'Erupção Vulcânica'),

        ('mar_violento', 'Mar Revolto'),
        ('ressaca', 'Ressaca Marinha'),

        ('poluicao', 'Poluição Ambiental'),
        ('nevoa_seca', 'Névoa Seca'),

        ('colapso_barragem', 'Colapso de Barragem'),
        ('contaminacao_agua', 'Contaminação da Água'),

        ('emergencia_quimica', 'Emergência Química'),
        ('emergencia_biologica', 'Emergência Biológica'),
        ('emergencia_nuclear', 'Emergência Nuclear'),
        
        ('outro', 'Outro'),
    )

    nome = models.CharField(max_length=200, verbose_name='Nome do evento')
    descricao = models.TextField(verbose_name='Descrição do evento')
    data_inicio = models.DateTimeField(verbose_name='Data de início')
    data_fim = models.DateTimeField(blank=True, null=True, verbose_name='Data de fim')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name='Tipo de evento')
    urgente = models.BooleanField(default=False, verbose_name='É urgente?')
    imagem = models.ImageField(upload_to='alertas/', blank=True, null=True, verbose_name='Imagem (deixar vazio irá usar uma imagem pré-definida)')
    paises = models.ManyToManyField(Pais, verbose_name='Paises afetados')
    estados = models.ManyToManyField(Estado, verbose_name='Estados afetados')
    cidades = models.ManyToManyField(Cidade, verbose_name='Cidades afetadas')
    doar = models.URLField(blank=True, null=True, verbose_name='Link para doação')

    def __str__(self):
        return self.nome

    def is_ocorrido(self):
        return self.data_fim < timezone.now()

    def is_em_andamento_ou_futuro(self):
        return self.data_fim >= timezone.now()
    
    def imagem_padrao(self):
        return f'imgs/eventos/{self.tipo}.png'
