from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from universitysystem.models import *
import datetime

def criarTurma(DisciplionaId, periodo, horariosSemanais, nome="", quantiaAulas=30):    
    disciplina = get_object_or_404(Disciplina, id=DisciplionaId)
    nomeTurma = nome if nome != "" else f"{disciplina.nome}"
    numeroTurma = Turma.objects.filter(
        disciplina=disciplina,
        periodo=periodo
    ).count() + 1

    novaTurma = Turma.objects.create(
        nome=nomeTurma,
        numero=numeroTurma,
        periodo=periodo,
        disciplina=disciplina,
        status=StatusDeTurma.FECHADA
    )

    # Criar aulas nos horários semanais
    aulasCriadas = 0
    dataAtual = min(horariosSemanais)  # pega a menor data como ponto inicial

    while aulasCriadas < quantiaAulas:
        for horario in horariosSemanais:
            if aulasCriadas >= quantiaAulas:
                break

            # Ajusta a data para a semana correta
            proximaData = dataAtual + datetime.timedelta(weeks=aulasCriadas // len(horariosSemanais))

            # Mantém o mesmo dia da semana e horário
            aulaDataHora = proximaData.replace(
                hour=horario.hour,
                minute=horario.minute,
                second=0,
                microsecond=0
            )

            Aula.objects.create(
                turma=novaTurma,
                data=aulaDataHora
            )
            aulasCriadas += 1

    return novaTurma

def abrirParaInscricoes(idTurma):
    turma = get_object_or_404(Turma, id=idTurma)
    turma.status = StatusDeTurma.ABERTA_PARA_INSCRICOES
    turma.save()

    return turma

def fecharInscricoes(idTurma):
    turma = get_object_or_404(Turma, id=idTurma)
    turma.status = StatusDeTurma.FECHADA
    turma.save()
    return turma

def iniciarTurma(idTurma):
    turma = get_object_or_404(Turma, id=idTurma)
    turma.status = StatusDeTurma.EM_ANDAMENTO
    turma.save()
    return turma

def getProfessores(idTurma):
    turma = get_object_or_404(Turma, id=idTurma)
    inscricoes = InscricaoDeProfessor.objects.filter(turma=turma)
    professores = [inscricao.professor for inscricao in inscricoes]
    return professores

def getAulas(idTurma):
    turma = get_object_or_404(Turma, id=idTurma)
    aulas = Aula.objects.filter(turma=turma).order_by('data')
    return aulas

def inscreverAluno(idTurma, idAluno):
    # OBS: Aceita o inscrição do aluno diretamente
    turma = get_object_or_404(Turma, id=idTurma)
    aluno = get_object_or_404(Aluno, id=idAluno)

    inscricao, created = InscricaoDeAluno.objects.get_or_create(
        aluno=aluno,
        turma=turma,        
    )

    if not created:
        inscricao.status = StatusDeMatriculaDeTurma.ACEITO
        inscricao.save()

    return inscricao

def cancelarInscricaoAluno(idTurma, idAluno):
    turma = get_object_or_404(Turma, id=idTurma)
    aluno = get_object_or_404(Aluno, id=idAluno)

    inscricao = get_object_or_404(InscricaoDeAluno,
        aluno=aluno,
        turma=turma
    )

    inscricao.delete()

    return 

def inscreverProfessor(idTurma, idProfessor):
    turma = get_object_or_404(Turma, id=idTurma)
    professor = get_object_or_404(Professor, id=idProfessor)

    inscricao, created = InscricaoDeProfessor.objects.get_or_create(
        professor=professor,
        turma=turma,        
    )

    return inscricao

def cancelarInscricaoProfessor(idTurma, idProfessor):
    turma = get_object_or_404(Turma, id=idTurma)
    professor = get_object_or_404(Professor, id=idProfessor)

    inscricao = get_object_or_404(InscricaoDeProfessor,
        professor=professor,
        turma=turma
    )

    inscricao.delete()

    return

