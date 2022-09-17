from django.contrib import admin
from .models import Incidente, Tipo_Incidente

# Register your models here.

admin.site.register(Incidente)
admin.site.register(Tipo_Incidente)