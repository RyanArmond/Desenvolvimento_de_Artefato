from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Aluno, RestauranteUniversitario
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import calendar
from datetime import date


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


def logout_view(request):
    logout(request)
    return redirect('login')