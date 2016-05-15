from django.contrib import admin
from .models import Coleccion, ContenidoMultimedia, AccionPelicula, \
    AccionSerie, AccionPersona


admin.site.register(Coleccion)
admin.site.register(ContenidoMultimedia)
admin.site.register(AccionPelicula)
admin.site.register(AccionSerie)
admin.site.register(AccionPersona)
