from django.shortcuts import render

from .models import Incidente, Municipio, Estado
from .serializers import IncidenteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ListaIncidentes(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        incidentes = Incidente.objects.all().order_by('-fecha')
        incidentes_json = IncidenteSerializer(incidentes, many=True) # Serializamos todos los incidentes a json
        return Response(incidentes_json.data, status=200) # Se envia el JSON como texto al cliente que lo solicita
    
    def post(self, request):
        dict = request.data.dict()
        dict.update({'publicador': request.user.id}) # Agrego al diccionario el id del usuario que publica el incidente
        incidente = IncidenteSerializer(data=dict) # Serializamos el diccionario a un objeto Incidente
        if incidente.is_valid(): # Si el incidente es valido
            incidente.save()
            return Response(incidente.data, status=200) # Retorno la informacion del incidente creado
        return Response(incidente.errors, status=400) # Retorno los errores que se pudieron dar en el transcurso de la validacion

    def put(self, request):
        incidente = Incidente.objects.get(id=request.POST.get('incidente'))
        if incidente:
            dict = request.data.dict()
            dict.update({'publicador': request.user.id}) # Debido a que no incluimos en el json el id del usuario, lo agregamos manualmente infiriendolo desde el token de autenticacion
            dict.pop('incidente') # Eliminamos el id del incidente del diccionario para evitar que cambie el id del incidente
            incidente = IncidenteSerializer(incidente, data=dict)
            if incidente.is_valid():
                incidente.save()
                return Response(incidente.data, status=200)
            else:
                return Response(incidente.errors, status=400)
        else:
            return Response({'message':'No se encontro el incidente'},status=400)

    def delete(self, request):
        incidente = Incidente.objects.get(id=request.POST.get('incidente'))
        if incidente and incidente.delete(): # Si encontramos un incidente que coincida y lo podemos eliminar
            return Response({'message':'Incidente eliminado correctamente'},status=200)
        return Response({'message':'No se pudo eliminar el incidente'},status=400)
        
class EstadoMunicipio(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, id_municipio):
        municipios = Municipio.objects.filter(id=id_municipio)
        if any(municipios):
            municipio = municipios.values('id','estado__nombre')
            return Response(municipio, status=200)
        return Response({'message':'No se encontro el municipio'},status=400)

class MunicipiosEstadoList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, id_estado):
        estados_disponibles = Estado.objects.all().values_list('id', flat=True)
        estados_disponibles = list(estados_disponibles)
        print(estados_disponibles)
        if id_estado not in estados_disponibles:
            return Response({'message':'No se encontro el estado'},status=400)
        
        municipios = Municipio.objects.filter(estado=id_estado)
        municipios = municipios.values('id','nombre')
        return Response(municipios, status=200)
        
class FiltrarIncidentes(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        incidentes = Incidente.objects.all()
        if request.POST.get('tipo_incidente'):
            incidentes = incidentes.filter(tipo_incidente=request.POST.get('tipo_incidente'))
        if request.POST.get('municipio'):
            incidentes = incidentes.filter(municipio=request.POST.get('municipio'))
        if request.POST.get('estado'):
            incidentes = incidentes.filter(municipio__estado=request.POST.get('estado'))
        if request.POST.get('fecha'):
            incidentes = incidentes.filter(fecha=request.POST.get('fecha'))
        incidentes_json = IncidenteSerializer(incidentes, many=True)
        return Response(incidentes_json.data, status=200)