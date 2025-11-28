from django.db import models
import sys

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Create your models here.
class StatusDeMatricula(models.TextChoices):
    ATIVA = 'A', 'Ativa'
    TRANCADA = 'T', 'Trancada'
    DESATIVADA = 'D', 'Desativada'
    CONCLUIDA = 'C', 'Concluida'

class StatusDeTurma(models.TextChoices):
    ABERTA_PARA_INSCRICOES = 'ABI', 'Aberta para Inscrições'
    FECHADA = 'FE', 'Fechada'
    EM_ANDAMENTO = 'EA', 'Em Andamento'
    ENCERRADA = 'EN', 'Encerrada'

class StatusDeMatriculaDeTurma(models.TextChoices):
    SOLICITACAO = 'SO', 'Solicitação'
    ACEITO = 'AC', 'Aceito'
    REJEITADO = 'RE', 'Rejeitado'

class Funcao(models.TextChoices):
    ALUNO = 'AL', 'Aluno'
    PROFESSOR = 'PR', 'Professor'
    COORDENADOR = 'CO', 'Coordenador'

class Usuario(models.Model):
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    senha = models.CharField(max_length=128, verbose_name="Senha")
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    foto_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL da Foto")
    tipo_usuario = models.CharField(max_length=20, verbose_name="Tipo de Usuário")
    matricula = models.CharField(max_length=20, unique=True, verbose_name="Matrícula")
    
    status = models.CharField(
        max_length=1,
        choices=StatusDeMatricula.choices,
        default=StatusDeMatricula.ATIVO,
        verbose_name="Status da Matrícula"
    )

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"


class Turma(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    numero = models.IntegerField(verbose_name="Número")
    periodo = models.IntegerField(verbose_name="Período")
    
    status = models.CharField(
        max_length=2,
        choices=StatusDeTurma.choices,
        default=StatusDeTurma.ABERTA,
        verbose_name="Status da Turma"
    )

    def __str__(self):
        return f"{self.nome} - {self.numero}"