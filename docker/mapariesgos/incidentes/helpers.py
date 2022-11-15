from .models import Incidente, Tipo_Incidente


def get_tipo_incidente_id(id):
    tipo_incidente = Tipo_Incidente.objects.filter(id=id)
    if any(tipo_incidente):
        return tipo_incidente.first()
    return None