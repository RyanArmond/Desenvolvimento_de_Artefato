from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate

def getTurmasDoCurso(request, idCurso):
    # TODO: Verificar se está logado    
    
    try:
        curso = Curso.objects.get(id=idCurso)
    except Curso.DoesNotExist:
        return HttpResponse("Curso não encontrado", status=404)
    
    turmas = Turma.objects.filter(disciplina__Curso=curso)
    
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

def getAgenda(request):
    # TODO: Verificar se está logado

    return