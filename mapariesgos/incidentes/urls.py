from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns=[
    path('login/', obtain_auth_token, name='api_token_auth'), # Esta es una url para realizar el login de un usuario existente, regresa un token drf para autorizar el uso de la api
    path('incidentes/', views.ListaIncidentes.as_view()), # Retorna la lista de todos los incidentes
    
]