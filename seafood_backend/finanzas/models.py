from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings

class CuentaContable(models.Model):
    TIPO_CHOICES = [
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
        ('capital', 'Capital'),
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cuenta_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'

class AsientoContable(models.Model):
    TIPO_CHOICES = [
        ('venta', 'Venta'),
        ('compra', 'Compra'),
        ('gasto', 'Gasto'),
        ('ajuste', 'Ajuste'),
        ('otro', 'Otro'),
    ]
    
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    referencia = models.CharField(max_length=50)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Asiento Contable'
        verbose_name_plural = 'Asientos Contables'
        ordering = ['-fecha', '-id']

    def __str__(self):
        return f'Asiento #{self.id} - {self.fecha}'

class LineaAsiento(models.Model):
    asiento = models.ForeignKey(AsientoContable, on_delete=models.CASCADE, related_name='lineas')
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=200)
    debe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Línea de Asiento'
        verbose_name_plural = 'Líneas de Asiento'

    def __str__(self):
        return f'{self.cuenta.nombre} - {self.debe if self.debe > 0 else self.haber}'

class Factura(models.Model):
    TIPO_CHOICES = [
        ('emitida', 'Emitida'),
        ('recibida', 'Recibida'),
    ]
    
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitida', 'Emitida'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    cliente = models.ForeignKey('clientes.Cliente', null=True, blank=True, on_delete=models.PROTECT)
    proveedor = models.ForeignKey('proveedores.Proveedor', null=True, blank=True, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    iva = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    notas = models.TextField(blank=True, null=True)
    asiento_contable = models.OneToOneField(AsientoContable, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision', '-numero']

    def __str__(self):
        return f'Factura {self.numero}'

class Pago(models.Model):
    METODO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('cheque', 'Cheque'),
    ]
    
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT, related_name='pagos')
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asiento_contable = models.OneToOneField(AsientoContable, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha']

    def __str__(self):
        return f'Pago {self.id} - {self.factura.numero}'