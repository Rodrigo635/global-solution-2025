from django.db import models

class Animal(models.Model):
    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    especie = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    altura = models.FloatField()
    peso = models.FloatField()
    profissao = models.CharField(max_length=100)
    animais = models.ManyToManyField(Animal)


    def __str__(self):
        return self.nome