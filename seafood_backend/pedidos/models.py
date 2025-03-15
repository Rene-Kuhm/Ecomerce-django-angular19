from django.db import models
from django.conf import settings
from inventario.models import Producto
from clientes.models import Cliente
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('furgon', 'Furgón Refrigerado'),
        ('camion', 'Camión Refrigerado'),
        ('van', 'Van Refrigerada'),
    ]
    
    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad = models.DecimalField(max_digits=8, decimal_places=2)  # en kg
    temperatura_min = models.IntegerField(validators=[MinValueValidator(-40), MaxValueValidator(10)])
    temperatura_max = models.IntegerField(validators=[MinValueValidator(-40), MaxValueValidator(10)])
    en_servicio = models.BooleanField(default=True)
    ultima_revision = models.DateField()
    proxima_revision = models.DateField()
    notas = models.TextField(blank=True, null=True)

class RutaEntrega(models.Model):
    ESTADO_CHOICES = [
        ('planificada', 'Planificada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    fecha_entrega = models.DateField()
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    conductor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificada')
    temperatura_promedio = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    hora_inicio = models.TimeField(null=True)
    hora_fin = models.TimeField(null=True)
    kilometraje_inicial = models.DecimalField(max_digits=8, decimal_places=2)
    kilometraje_final = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    notas = models.TextField(blank=True, null=True)

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('en_ruta', 'En Ruta'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ruta_entrega = models.ForeignKey(RutaEntrega, on_delete=models.SET_NULL, null=True, blank=True)
    temperatura_entrega = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    hora_entrega = models.TimeField(null=True, blank=True)
    firma_cliente = models.ImageField(upload_to='firmas/', null=True, blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nombre}'

    def actualizar_total(self):
        total = sum(item.subtotal() for item in self.detalles.all())
        self.total = total
        self.save()

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    temperatura_empaque = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    lote = models.CharField(max_length=50, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} {self.producto.unidad}'

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio
        super().save(*args, **kwargs)
        self.pedido.actualizar_total()
