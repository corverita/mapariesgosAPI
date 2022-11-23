from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns=[
    path('login/', views.LoginUsuario.as_view(), name="login"), # Esta es la url para el login. de los usuarios
    path('logout/', views.LogoutUsuario.as_view(), name="logout"), # Esta es la url para el logout. de los usuarios
    # path('registro/', views.Registro.as_view(), name="registro"), # Esta es la url para el registro. de los usuarios
    
]