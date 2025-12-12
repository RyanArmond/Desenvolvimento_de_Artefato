from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from universitysystem.models import *
import datetime

def matricularProfessor(idUser, Email, Nome):
    user = get_object_or_404(Usuario, id=idUser)
    professor, created = Professor.objects.get_or_create(user=user)

    if created:
        professor.email = Email
        professor.nome_completo = Nome
        professor.save()
    return professor

def getTurmasDoProfessor(idUser):
    usuario = get_object_or_404(Usuario, id=idUser)
    professor = get_object_or_404(Professor, user=usuario)
    matriculas = InscricaoDeProfessor.objects.filter(
        professor=professor,
        turma__status='EA'
    )                
    turmas = [matricula.turma for matricula in matriculas]    
    return turmas