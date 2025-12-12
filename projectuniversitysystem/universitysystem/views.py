from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Aluno, RestauranteUniversitario, Usuario, Historico, ItemHistorico
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib import messages
import logging
import calendar
from datetime import date
from collections import defaultdict


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    return render(request, "home.html")


def restaurante_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    
    try:
        aluno = Aluno.objects.filter(user=request.user).first()

        if aluno and aluno.curso:
            instituicao_do_aluno = aluno.curso.instituicao
            
            ru = RestauranteUniversitario.objects.get(instituicao=instituicao_do_aluno)
            
            context['restaurante'] = ru
        else:
            context['erro'] = "Aluno não vinculado a um curso ou instituição."

    except RestauranteUniversitario.DoesNotExist:
        context['erro'] = "Ainda não há cardápio cadastrado para sua instituição."

    return render(request, 'restaurante.html', context)


def login_view(request):
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home_view') 
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@csrf_exempt
def login_google_view(request):
    if request.method == 'POST':

        token = request.POST.get("credential")

        try:
            data = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID,
                clock_skew_in_seconds=300  # tolera até 5 minutos de diferença
            )
            
            email = data["email"]
            name = data.get("name", "")

            user, _ = Usuario.objects.get_or_create(
                username=email,
                defaults={"first_name": name.split()[0], "last_name": " ".join(name.split()[1:])}
            )

            login(request, user)
            return redirect("home_view")
            
        except ValueError:
            logging.exception("Erro ao verificar token Google")
            return HttpResponse(status=403)


def logout_view(request):
    logout(request)
    return redirect('login')


def notas_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    
    aluno = Aluno.objects.filter(user=request.user).first()

    if aluno:
        try:
            historico = Historico.objects.get(aluno=aluno)
            
            itens = ItemHistorico.objects.filter(historico=historico).order_by('-periodo_cursado', 'disciplina__nome')
            
            boletim = defaultdict(list)
            for item in itens:
                boletim[item.periodo_cursado].append(item)
            
            context['boletim'] = dict(boletim)
            context['aluno'] = aluno

        except Historico.DoesNotExist:
            context['erro'] = "Histórico acadêmico não encontrado."
    else:
        context['erro'] = "Perfil de aluno não encontrado."

    return render(request, 'notas.html', context)


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        aluno = Aluno.objects.get(user=request.user)
        context = {'aluno': aluno}

    except Aluno.DoesNotExist:
        messages.error(request, "Aluno não encontrado. ")
        return redirect("home_view")
        
    return render(request, 'perfil.html', context)


def historico_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    aluno = get_object_or_404(Aluno, user=request.user)
    
    try:
        historico = Historico.objects.get(aluno=aluno)
        itens = ItemHistorico.objects.filter(historico=historico).select_related('disciplina').order_by('-periodo_cursado')
    except Historico.DoesNotExist:
        historico = None
        itens = []

    historico_agrupado = {}
    soma_notas = 0
    total_disciplinas = 0

    for item in itens:
        if item.periodo_cursado not in historico_agrupado:
            historico_agrupado[item.periodo_cursado] = []
        historico_agrupado[item.periodo_cursado].append(item)
        
        soma_notas += item.media
        total_disciplinas += 1

    ira = round(soma_notas / total_disciplinas, 2) if total_disciplinas > 0 else 0.0

    context = {
        'aluno': aluno,
        'historico_agrupado': historico_agrupado,
        'ira': ira,
    }
    
    return render(request, 'historico.html', context)