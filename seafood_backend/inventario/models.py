from django.db import models
from simple_history.models import HistoricalRecords
import uuid
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    historial = HistoricalRecords()
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre

def generate_unique_code():
    # Generar código único basado en timestamp y uuid
    timestamp = timezone.now().strftime('%y%m%d')
    unique_id = str(uuid.uuid4())[:6].upper()
    return f"PROD-{timestamp}-{unique_id}"

class Producto(models.Model):
    UNIDAD_CHOICES = [
        ('kg', 'Kilogramos'),
        ('lb', 'Libras'),
        ('unidad', 'Unidad'),
        ('caja', 'Caja'),
    ]
    
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(
        max_length=50,
        unique=True,
        default=generate_unique_code,
        help_text="Código único del producto generado automáticamente"
    )
    codigo_lote = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad = models.CharField(max_length=10, choices=UNIDAD_CHOICES, default='kg')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    historial = HistoricalRecords()
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    @property
    def margen_ganancia(self):
        if self.costo > 0:
            return ((self.precio - self.costo) / self.precio) * 100
        return 0

class PuntoControlHACCP(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    limite_critico = models.CharField(max_length=200)
    medida_correctiva = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    historial = HistoricalRecords()

    class Meta:
        verbose_name = "Punto de Control HACCP"
        verbose_name_plural = "Puntos de Control HACCP"

    def __str__(self):
        return self.nombre

class RegistroCalidad(models.Model):
    ESTADO_CHOICES = [
        ('conforme', 'Conforme'),
        ('no_conforme', 'No Conforme'),
        ('pendiente', 'Pendiente de Revisión')
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    punto_control = models.ForeignKey(PuntoControlHACCP, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    valor_medido = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)
    historial = HistoricalRecords()

    class Meta:
        verbose_name = "Registro de Calidad"
        verbose_name_plural = "Registros de Calidad"

    def __str__(self):
        return f"Control {self.punto_control} - {self.producto} - {self.fecha_registro}"

class Incidencia(models.Model):
    SEVERIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica')
    ]
    
    ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada')
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_deteccion = models.DateTimeField(auto_now_add=True)
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierta')
    accion_correctiva = models.TextField(blank=True, null=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    historial = HistoricalRecords()

    class Meta:
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"

    def __str__(self):
        return f"{self.titulo} - {self.producto}"