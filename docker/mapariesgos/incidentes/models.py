from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Estado(models.Model):
    clave = models.CharField('Clave Estado', max_length=2, unique=True, blank=False, null=False)
    nombre = models.CharField('nombre', max_length=50, unique=True, blank=False, null=False)
    abrev = models.CharField('abrev', max_length=10, unique=True, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Municipio(models.Model):
    clave = models.CharField('Clave Municipio', max_length=3, blank=False, null=False)
    nombre = models.CharField('nombre', max_length=150, blank=False, null=False)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Tipo_Incidente(models.Model):
    icono = models.ImageField('Ruta al icono')
    nombre = models.CharField('nombre', max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Incidente(models.Model):
    latitud = models.DecimalField('latitud',blank=False, null=False, max_digits=50, decimal_places=20)
    longitud = models.DecimalField('longitud', blank=False, null=False, max_digits=50, decimal_places=20)
    fecha = models.DateTimeField('Fecha', blank=False, null=False, auto_now_add=timezone.now)
    publicador = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
    tipo_incidente = models.ForeignKey(Tipo_Incidente, on_delete=models.PROTECT, blank=False, null=False)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, blank=False, null=False, default = 2400)
    
    def __str__(self):
        return f"{self.tipo_incidente} {self.fecha}"