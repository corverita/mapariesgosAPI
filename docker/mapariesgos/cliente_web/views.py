import json
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages

from incidentes.models import Incidente, Estado, Municipio
from incidentes.serializers import IncidenteSerializer
from .utils import iconos

# Create your views here.

def home(request):
    incidentes = Incidente.objects.all() #TODO limitar la cantidad de incidentes que se muestran en un inicio.
    lista_incidentes = []
    for incidente in incidentes:
        incidente.icon = iconos[str(incidente.tipo_incidente)]
        lista_incidentes.append(IncidenteSerializer(incidente).data)
    
    context = {
        'incidentes' : incidentes,
        'lista_incidentes' : lista_incidentes,
        'API_KEY': '',
        'estados': Estado.objects.all(),
        'municipios': Municipio.objects.all(),
    }
    return render(request, 'home.html', context)