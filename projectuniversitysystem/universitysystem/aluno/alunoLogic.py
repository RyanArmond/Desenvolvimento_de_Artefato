from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q

# Verificar antes se é aluno e está logado; Não ocorre verificação nessa função
def getTurmasAtuaisUnsafe(User):
    usuario = User
    aluno = get_object_or_404(Aluno, user=usuario)
    matriculas = MatriculaEmTurma.objects.filter(
        aluno=aluno,
        status='AC',
        turma__status='EA'
    )
    turmas = [matricula.turma for matricula in matriculas]
    return turmas

def getTurmasDoAluno(request):
    # TODO: Verificar se está logado
    # TODO: Verificar se é um aluno
  
    turmas = getTurmasAtuaisUnsafe(request)

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
    # TODO: Verificar se é um aluno

    turmas = getTurmasAtuaisUnsafe(request)
    avisos = Aviso.objects.filter(turma__in=turmas).order_by('-data')
    json = [
        {
            "id": aviso.id,
            "turma": aviso.turma.nome,
            "turma_id": aviso.turma.id,
            "titulo": aviso.titulo,
            "descricao": aviso.descricao,
            "data": aviso.data,
        }
        for aviso in avisos
    ]

    return JsonResponse(json, safe=False)

def getAvisosDaTurma(request, idTurma):    
    turmaEsc = get_object_or_404(Turma, id=idTurma)
    avisos = Aviso.objects.filter(turma=turmaEsc).order_by('-data')

    json = [
        {
            "id": aviso.id,
            "turma": aviso.turma.nome,
            "turma_id": aviso.turma.id,
            "titulo": aviso.titulo,
            "descricao": aviso.descricao,
            "data": aviso.data,
        }
        for aviso in avisos
    ]

    return JsonResponse(json, safe=False)

def getInformacoes(request):
    # TODO: Verificar se está logado
    # TODO: Verificar se é um aluno

    # TODO: Verificar a média do aluno
    # TODO: Retornar a matrícula, nome completo e email
    # TODO: Retornar curso do aluno

    return