from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
