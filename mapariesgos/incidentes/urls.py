from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns=[
    path('login/', obtain_auth_token), # Esta es una url para realizar el login de un usuario existente, regresa un token drf para autorizar el uso de la api
    path('incidentes/', views.ListaIncidentes.as_view()), # Retorna la lista de todos los incidentes
    path('municipios/<int:id_estado>/', views.MunicipiosEstadoList.as_view()), # Retorna la lista de municipios de un estado
    path('estado-municipio/<int:id_municipio>/', views.EstadoMunicipio.as_view()), # Retorna el estado de un municipio
    path('filtrar-incidentes/', views.FiltrarIncidentes.as_view()), # Retorna la lista de incidentes filtrados por los parametros enviados
    
]