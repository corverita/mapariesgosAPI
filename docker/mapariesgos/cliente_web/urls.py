from django.urls import path
from . import views

app_name = 'web'

urlpatterns=[
    path('', views.home, name="home"), # Esta es la url base, donde todos tendran acceso al mapa
    # path('filtrar-incidentes/', views.filtrar_incidentes, name="filtrar-incidentes"), # Esta es la url para el filtrado de incidentes
    # path('reportar-incidente/<int:id_incidente>', views.reportar_incidente, name="reportar-incidente"), # Esta es la url para el reporte de incidentes
    
]