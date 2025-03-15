from django.contrib import admin
from .models import Producto, Categoria, PuntoControlHACCP, RegistroCalidad, Incidencia

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cantidad_stock', 'activo')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre', 'descripcion', 'codigo', 'codigo_lote')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

@admin.register(PuntoControlHACCP)
class PuntoControlHACCPAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'limite_critico', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

@admin.register(RegistroCalidad)
class RegistroCalidadAdmin(admin.ModelAdmin):
    list_display = ('producto', 'punto_control', 'fecha_registro', 'estado')
    list_filter = ('estado', 'punto_control')
    search_fields = ('producto__nombre', 'observaciones')
    readonly_fields = ('fecha_registro',)

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'producto', 'severidad', 'estado', 'fecha_deteccion')
    list_filter = ('severidad', 'estado')
    search_fields = ('titulo', 'descripcion', 'producto__nombre')
    readonly_fields = ('fecha_deteccion', 'fecha_resolucion')
