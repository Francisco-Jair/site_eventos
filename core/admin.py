from django.contrib import admin
from .models import Palestrantes, Minicursos, Usuarios

admin.site.register(Palestrantes)
admin.site.register(Minicursos)
admin.site.register(Usuarios)