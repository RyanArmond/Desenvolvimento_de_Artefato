from django.shortcuts import render
from django.http import HttpResponseRedirect
#from .models import nomedomodel1,nomedomodel2
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
import calendar
from datetime import date #criar calendario
# Create your views here.
