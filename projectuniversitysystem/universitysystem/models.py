from django.db import models
import sys

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Create your models here.
class Disciplina(models.Model):
    ID = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=256)
    Codigo = models.CharField(max_length=16)
    Descricao = models.TextField()                   
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

class Curso(models.Model):
    ID = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=256)
    Descricao = models.TextField()           
    Sigla = models.CharField(max_length=16)
    Horarios = models.CharField(max_length=32)
    Instituicao = models.ForeignKey(Instituicao, on_delete=models.PROTECT)

class Instituicao(models.Model):
    ID = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=256)
    Sigla = models.CharField(max_length=16)
    CNPJ = models.CharField(max_length=32)
    Endereco = models.CharField(max_length=512)    