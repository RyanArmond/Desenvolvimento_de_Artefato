from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
import calendar
from datetime import date #criar calendario
# Create your views here.

def index(request):
    return HttpResponse("<h1>Olá Mundo! 🚀</h1><p>Tela Teste.</p>")