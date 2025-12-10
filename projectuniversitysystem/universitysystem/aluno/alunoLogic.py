from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q

def getTurmasDoAluno(request):
    # TODO: Verificar se está logado
    # TODO: Verificar se é um aluno

    usuario = request.user
    aluno = get_object_or_404(Aluno, user=usuario)
    matriculas = MatriculaEmTurma.objects.filter(
        aluno=aluno,
        status='AC',
        turma__status='EA'
    )
    turmas = [matricula.turma for matricula in matriculas]

    json = [
        {
            "id": turma.id,
            "nome": turma.nome,
            "numero": turma.numero,
            "periodo": turma.periodo,
            "status": turma.status,
        }
        for turma in turmas
    ]

    return JsonResponse(json, safe=False)    

def getTurmasAntigas(request):
    # TODO: Verificar se está logado
    # TODO: Verificar se é um aluno

    usuario = request.user
    aluno = get_object_or_404(Aluno, user=usuario)
    matriculas = MatriculaEmTurma.objects.filter(
        aluno=aluno,
        status='AC',        
    ).filter(
        Q(turma__status='EN') | Q(turma__status='FE') 
    )

    turmas = [matricula.turma for matricula in matriculas]

    json = [
        {
            "id": turma.id,
            "nome": turma.nome,
            "numero": turma.numero,
            "periodo": turma.periodo,
            "status": turma.status,
        }
        for turma in turmas
    ]

    return JsonResponse(json, safe=False)

def getAvisos(request):
    # TODO: Verificar se está logado    
    return

def getAgenda(request):
    # TODO: Verificar se está logado
    return

def getInformacoes(request):
    # TODO: Verificar se está logado
    return