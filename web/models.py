from django.contrib import admin
from django.db import models
from matplotlib import ticker

# Create your models here.
class Acao(models.Model):
    ticker = models.CharField(max_length=500)
    nome = models.CharField(max_length=500)
    preco = models.FloatField()

    def __str__(self):
        return self.nome

admin.site.register(Acao)