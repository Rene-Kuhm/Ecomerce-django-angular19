from django.db import models
from django.conf import settings
from inventario.models import Producto
from clientes.models import Cliente

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades'

    def subtotal(self):
        return self.cantidad * self.precio_unitario
