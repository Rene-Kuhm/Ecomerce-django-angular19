from django.contrib import admin
from .models import Informe

@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_creacion', 'creado_por')
    list_filter = ('tipo', 'fecha_creacion', 'creado_por')
    search_fields = ('titulo', 'creado_por__username')
    readonly_fields = ('fecha_creacion', 'creado_por', 'contenido')
