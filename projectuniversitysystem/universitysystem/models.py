from django.db import models
from django.contrib.auth.models import AbstractUser
import sys

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Create your models here.
class Instituicao(models.Model):
    Nome = models.CharField(max_length=256)
    Sigla = models.CharField(max_length=16)
    CNPJ = models.CharField(max_length=32)
    Endereco = models.CharField(max_length=512)  

class Curso(models.Model):
    Nome = models.CharField(max_length=256)
    Descricao = models.TextField()           
    Sigla = models.CharField(max_length=16)
    Horarios = models.CharField(max_length=32)
    Instituicao = models.ForeignKey(Instituicao, on_delete=models.PROTECT)

class Disciplina(models.Model):
    Nome = models.CharField(max_length=256)
    Codigo = models.CharField(max_length=16)
    Descricao = models.TextField()                   
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  

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

class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    foto_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL da Foto")

    funcao = models.CharField(
        null=False,
        max_length=2,
        choices=Funcao.choices,
        default=Funcao.ALUNO,
        verbose_name="Função"
    )
    

class Aluno(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    matricula = models.IntegerField(verbose_name="Matrícula")
    
    status = models.CharField(
        max_length=1,
        choices=StatusDeMatricula.choices,
        default=StatusDeMatricula.ATIVA,
        verbose_name="Status da Matrícula"
    )

    REQUIRED_FIELDS = ['email', 'cpf', 'matricula']

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"

class Professor(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)    
    email = models.EmailField(unique=True, verbose_name="E-mail")
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")        

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"
    
class Coordenador(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)    
    email = models.EmailField(unique=True, verbose_name="E-mail")
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")        

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"

class Turma(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    numero = models.IntegerField(verbose_name="Número")
    periodo = models.IntegerField(verbose_name="Período")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length=3,
        choices=StatusDeTurma.choices,
        default=StatusDeTurma.ABERTA_PARA_INSCRICOES,
        verbose_name="Status da Turma"
    )

    def __str__(self):
        return f"{self.nome} - {self.numero}"
    
class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)   
    titulo = models.CharField(max_length=256)
    descricao = models.TextField()
    data = models.DateField() 

class Anexo(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)   
    nome = models.TextField()
    arquivo_url = models.URLField(max_length=512)    

class Aviso(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)   
    titulo = models.CharField(max_length=256)
    descricao = models.TextField()
    data = models.DateField()

class InscricaoDeAluno(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length=2,
        choices=StatusDeMatriculaDeTurma.choices,
        default=StatusDeMatriculaDeTurma.SOLICITACAO,
        verbose_name="Status de inscrição"
    )

class InscricaoDeProfessor(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)    