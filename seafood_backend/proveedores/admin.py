from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'contacto', 'email', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'rut', 'email', 'contacto')
    date_hierarchy = 'fecha_registro'
