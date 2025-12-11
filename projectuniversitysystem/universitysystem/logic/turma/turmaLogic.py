from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from universitysystem.models import *

def criarTurma(DisciplionaId, periodo, horariosSemanais, nome = "", quantiaAulas = 30):    
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

    # TODO: Criar as aulas nos horários semanais

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

