from .models import Incidente, Municipio
from cliente_web.utils import iconos

from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        
class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ['nombre', 'estado']
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['estado'] = instance.estado.nombre
        return response

class IncidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Incidente
        fields = ['id','latitud','longitud','fecha','publicador','tipo_incidente', 'municipio', 'estado_actual']
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['publicador'] = UserSerializer(instance.publicador).data
        response['tipo_incidente'] = instance.tipo_incidente.nombre
        response['municipio'] = MunicipioSerializer(instance.municipio).data
        response['icon'] = iconos[str(instance.tipo_incidente)]
        return response
    
    def create(self, validated_data):
        return Incidente.objects.create(**validated_data)