from django.shortcuts import render

from incidentes.models import Incidente
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def home(request):
    context = {
        'incidentes' : Incidente.objects.all(),
        'API-KEY': 'Llave'
    }
    return render(request, 'home.html')