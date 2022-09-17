from django.shortcuts import render

from .models import Incidente
from .serializers import IncidenteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ListaIncidentes(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        incidentes = Incidente.objects.all()
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
        else:
            return Response({'message':'No se pudo eliminar el incidente'},status=400)