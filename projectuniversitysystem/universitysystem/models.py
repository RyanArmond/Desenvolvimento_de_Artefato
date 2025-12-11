from django.db import models
from django.contrib.auth.models import AbstractUser
import sys

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# ENUMS
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
    ADMIN = 'AD', 'Admin'


class TipoCompromisso(models.TextChoices):
    FERIADO = "FE", "Feriado"
    INICIO_AULAS = "IA", "Início das Aulas"
    FIM_AULAS = "FA", "Fim das Aulas"
    PROVA = "PR", "Prova"
    EVENTO = "EV", "Evento"
    RECESSO = "RE", "Recesso"
#FIM ENUMS

class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    foto_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL da Foto")
    matricula = models.CharField(max_length=50, unique=True, verbose_name="Matrícula")
    
    funcao = models.CharField(
        null=False,
        max_length=2,
        choices=Funcao.choices,
        default=Funcao.ALUNO,
        verbose_name="Função"
    )
    
    REQUIRED_FIELDS = ['cpf', 'matricula']

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['first_name', 'username']
    
    def __str__(self):
        nome_de_exibicao = self.get_full_name()
        
        if not nome_de_exibicao:
            nome_de_exibicao = self.username
        
        return f'{nome_de_exibicao} ({self.matricula})'


class Instituicao(models.Model):
    nome = models.CharField(max_length=256)
    sigla = models.CharField(max_length=16)
    cnpj = models.CharField(max_length=32)
    endereco = models.CharField(max_length=512)  

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Curso(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.PROTECT, verbose_name="Instituição")
    
    nome = models.CharField(max_length=256)
    descricao = models.TextField()           
    sigla = models.CharField(max_length=16)
    horarios = models.CharField(max_length=32, verbose_name="Horários")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['instituicao__nome','nome']
        
    def __str__(self):
        return f"{self.nome} - {self.instituicao.nome}"


class Aluno(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, null=True, verbose_name="Curso")
    
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    matricula = models.CharField(max_length=50, verbose_name="Matrícula")
    
    status = models.CharField(
        max_length=1,
        choices=StatusDeMatricula.choices,
        default=StatusDeMatricula.ATIVA,
        verbose_name="Status da Matrícula"
    )

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome_completo']
    
    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"


class Disciplina(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  
    
    nome = models.CharField(max_length=256)
    codigo = models.CharField(max_length=16)
    descricao = models.TextField()                   
    
    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['curso__instituicao__nome', 'curso__nome', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.codigo})"
    

class Turma(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    numero = models.IntegerField(verbose_name="Número")
    periodo = models.IntegerField(verbose_name="Período")
    
    status = models.CharField(
        max_length=3,
        choices=StatusDeTurma.choices,
        default=StatusDeTurma.ABERTA_PARA_INSCRICOES,
        verbose_name="Status da Turma"
    )

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ['-periodo', 'nome']

    def __str__(self):
        return f"{self.nome} - Turma {self.numero} ({self.periodo})"


class Historico(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    data_emissao = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = 'Histórico'
        verbose_name_plural = 'Históricos'
    
    def __str__(self):
        return f"Historico de {self.aluno}"
    
    
class ItemHistorico(models.Model):
    historico = models.ForeignKey(Historico, on_delete=models.CASCADE, related_name="itens")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    
    media = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Média Final")
    
    periodo_cursado = models.CharField(max_length=6, help_text="Ex: 2025.2")
    
    class Meta:
        unique_together = ('historico', 'disciplina')
        verbose_name = "Item do Histórico"
        verbose_name_plural = "Itens do Histórico"
        
    def __str__(self):
        return f"{self.discilina.nome}: {self.media}"
    

class RestauranteUniversitario(models.Model):
    instituicao = models.OneToOneField(Instituicao, on_delete=models.CASCADE)
    
    cafe_manha = models.TextField(verbose_name="Café da Manhã", blank=True, default="Não informado")
    almoco = models.TextField(verbose_name="Almoço", blank=True, default="Não informado")
    jantar = models.TextField(verbose_name="Jantar", blank=True, default="Não informado")
    horario_funcionamento = models.TextField(verbose_name="Horário de Funcionamento")
    precos = models.TextField(verbose_name="Tabela de Preços")
    
    class Meta:
        verbose_name = "Restaurante Universitário"
        verbose_name_plural = "Restaurantes Universitários"
        
    def __str__(self):
        return f"RU - {self.instituicao.sigla}"    
    

class CalendarioAcademico(models.Model):
    data_referencia = models.DateField(verbose_name="Data de Referência")
    descricao = models.CharField(max_length=100, blank=True, verbose_name="Descrição", help_text="Ex: Calendário Acadêmico 2025.2")
    
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Calendário Acadêmico"    
        verbose_name_plural = "Calendários Acadêmicos"
        ordering = ['-data_referencia']

    def __str__(self):
        return f"Calendário {self.data_referencia.strftime("%Y")}"

    
class Compromisso(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título")
    data = models.DateField(verbose_name="Data do Compromisso")
    
    calendario_academico = models.ForeignKey(CalendarioAcademico, on_delete=models.CASCADE, related_name='compromissos')

    tipo = models.CharField(
        max_length=2,
        choices=TipoCompromisso.choices,
        default=TipoCompromisso.EVENTO,
        verbose_name="Tipo do Compromisso"
    )
    
    class Meta:
        verbose_name = "Compromisso"
        verbose_name_plural = "Compromissos"
        ordering = ["data"]
        
    def __str__(self):
        return f"{self.data.strftime("%d/%m")} - {self.titulo}"
    
    
