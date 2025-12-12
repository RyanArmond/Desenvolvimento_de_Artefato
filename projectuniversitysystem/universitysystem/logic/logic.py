from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from universitysystem.models import *

def getTurmasDoCurso(request, idCurso):    
    try:
        curso = Curso.objects.get(id=idCurso)
    except Curso.DoesNotExist:
        return HttpResponse("Curso não encontrado", status=404)
    
    turmas = Turma.objects.filter(disciplina__Curso=curso)

    return turmas;

def getAgenda(request):
    # TODO: Verificar se está logado

    return