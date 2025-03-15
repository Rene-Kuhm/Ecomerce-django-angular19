from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'email', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'rut', 'email')
    date_hierarchy = 'fecha_registro'
