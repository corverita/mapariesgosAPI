from django.shortcuts import render
from django.views.generic import DetailView

from .models import Estado_Actual, Incidente, Municipio, Estado
from .serializers import IncidenteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.

def incidente_detail(request, id_incidente):
    incidente = Incidente.objects.filter(id=id_incidente)
    incidente_json = IncidenteSerializer(incidente, many=True)
    return Response(incidente_json.data, status=200)

class DetalleIncidente(DetailView):
    model = Incidente
    template_name = 'modal_info_incidente.html'
    context_object_name = 'incidente'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({'estados_actuales': Estado_Actual.objects.all})
        return context

class ListaIncidentes(APIView):
    
    def get(self, request):
        incidentes = Incidente.objects.all().order_by('-fecha')
        incidentes_json = IncidenteSerializer(incidentes, many=True) # Serializamos todos los incidentes a json
        return Response(incidentes_json.data, status=200) # Se envia el JSON como texto al cliente que lo solicita
    
    def post(self, request):
        dict = request.data.dict()
        dict.pop('direccion')
        dict.update({'publicador': request.user.id}) # Agrego al diccionario el id del usuario que publica el incidente
        estados = Estado.objects.filter(nombre=dict['estado'])
        dict.update({'estado': estados.first().id if any(estados) else -1}) # Agrego al diccionario el estado del incidente
        municipios = Municipio.objects.filter(nombre=dict['municipio'], estado=dict['estado'])
        dict.update({'municipio': municipios.first().id if any(municipios) else -1}) # Agrego al diccionario el municipio del incidente (si no existe el municipio, se asigna -1 y devuelve el error)
        dict.update({'latitud': float(dict['latitud'])}) # Convierto en el diccionario la latitud del incidente
        dict.update({'longitud': float(dict['longitud'])}) # Convierto en el diccionario la longitud del incidente
        dict.update({'tipo_incidente': int(dict['tipo_incidente'])}) # Convierto en el diccionario el tipo de incidente
        dict.update({'estado_actual': Estado_Actual.objects.get(descripcion='Activo').id})
        
        incidente = IncidenteSerializer(data=dict) # Serializamos el diccionario a un objeto Incidente
        if incidente.is_valid(): # Si el incidente es valido
            incidente.save()
            return Response(incidente.data, status=200) # Retorno la informacion del incidente creado
        response = {
            'status': 'Bad request',
            'message': 'Hubo un problema al registrar el incidente.',
            'errors': incidente.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST) # Retorno los errores que se pudieron dar en el transcurso de la validacion

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
    
    def get(self, request, id_municipio):
        municipios = Municipio.objects.filter(id=id_municipio)
        if any(municipios):
            municipio = municipios.values('id','estado__nombre')
            return Response(municipio, status=200)
        return Response({'message':'No se encontro el municipio'},status=400)

class MunicipiosEstadoList(APIView):
    
    def get(self, request, id_estado):
        estados_disponibles = Estado.objects.all().values_list('id', flat=True)
        estados_disponibles = list(estados_disponibles)
        if id_estado not in estados_disponibles:
            return Response({'message':'No se encontro el estado'},status=400)
        
        municipios = Municipio.objects.filter(estado=id_estado)
        municipios = municipios.values('id','nombre')
        return Response(municipios, status=200)
        
class FiltrarIncidentes(APIView):
    
    def post(self, request):
        incidentes = Incidente.objects.all().order_by('-fecha')
        if request.POST.get('tipo_incidente') and int(request.POST.get('tipo_incidente')) > 0:
            incidentes = incidentes.filter(tipo_incidente=request.POST.get('tipo_incidente'))
            
        if request.POST.get('estado') and int(request.POST.get('estado')) > 0:
            incidentes = incidentes.filter(municipio__estado=request.POST.get('estado'))
            
        if request.POST.get('municipio') and int(request.POST.get('municipio')) > 0:
            incidentes = incidentes.filter(municipio=request.POST.get('municipio'))
            
        if request.POST.get('fecha'):
            incidentes = incidentes.filter(fecha__date=request.POST.get('fecha'))
        incidentes_json = IncidenteSerializer(incidentes, many=True)
        return Response(incidentes_json.data, status=200)