from django.contrib import admin
from .models import Usuarios, Colecciones, ContenidoMultimedia, Comentarios, \
    MensajesTablon, Amigos, Acciones

admin.site.register(Usuarios)
admin.site.register(Colecciones)
admin.site.register(ContenidoMultimedia)
admin.site.register(Comentarios)
admin.site.register(MensajesTablon)
admin.site.register(Amigos)
admin.site.register(Acciones)
