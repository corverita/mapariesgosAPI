from django.forms import ModelForm

from incidentes.models import Incidente

class IncidenteForm(ModelForm):
    class Meta:
        model = Incidente
        fields = ['latitud','longitud','tipo_incidente']
    