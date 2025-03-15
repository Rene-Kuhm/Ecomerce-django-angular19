from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator

class Informe(models.Model):
    TIPO_CHOICES = [
        ('ventas', 'Informe de Ventas'),
        ('inventario', 'Informe de Inventario'),
        ('clientes', 'Informe de Clientes'),
        ('proveedores', 'Informe de Proveedores'),
        ('prediccion', 'Predicción de Demanda'),
        ('tendencias', 'Análisis de Tendencias'),
        ('kpis', 'Indicadores de Desempeño'),
    ]
    
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.JSONField()
    
    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"

class PrediccionDemanda(models.Model):
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    demanda_predicha = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    intervalo_confianza_bajo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    intervalo_confianza_alto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    factores_estacionales = models.JSONField()
    variables_externas = models.JSONField(default=dict)
    precision_modelo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Predicción de Demanda'
        verbose_name_plural = 'Predicciones de Demanda'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"Predicción {self.producto.nombre} ({self.fecha_inicio} - {self.fecha_fin})"

class IndicadorDesempeno(models.Model):
    CATEGORIA_CHOICES = [
        ('financiero', 'Financiero'),
        ('operacional', 'Operacional'),
        ('calidad', 'Calidad'),
        ('logistica', 'Logística'),
        ('ventas', 'Ventas'),
    ]
    
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField()
    formula = models.TextField()
    unidad = models.CharField(max_length=50)
    valor_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Indicador de Desempeño'
        verbose_name_plural = 'Indicadores de Desempeño'
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

class RegistroKPI(models.Model):
    indicador = models.ForeignKey(IndicadorDesempeno, on_delete=models.CASCADE)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Registro de KPI'
        verbose_name_plural = 'Registros de KPIs'
        ordering = ['-fecha']
        unique_together = ['indicador', 'fecha']
    
    def __str__(self):
        return f"{self.indicador.nombre} - {self.fecha}"
        
    def estado(self):
        if self.valor >= self.indicador.valor_objetivo:
            return 'óptimo'
        elif self.valor >= self.indicador.valor_minimo:
            return 'aceptable'
        else:
            return 'crítico'

class RegistroSostenibilidad(models.Model):
    TIPO_REGISTRO_CHOICES = [
        ('energia', 'Consumo Energético'),
        ('agua', 'Consumo de Agua'),
        ('residuos', 'Generación de Residuos'),
        ('emisiones', 'Emisiones de CO2'),
        ('reciclaje', 'Material Reciclado'),
    ]
    
    fecha = models.DateField()
    tipo_registro = models.CharField(max_length=20, choices=TIPO_REGISTRO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    notas = models.TextField(blank=True, null=True)
    evidencia = models.FileField(upload_to='sostenibilidad/evidencias/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Registro de Sostenibilidad'
        verbose_name_plural = 'Registros de Sostenibilidad'
        ordering = ['-fecha']
        
    def __str__(self):
        return f"{self.get_tipo_registro_display()} - {self.fecha}"

class CertificacionAmbiental(models.Model):
    ESTADO_CHOICES = [
        ('en_proceso', 'En Proceso'),
        ('obtenida', 'Obtenida'),
        ('renovacion', 'En Renovación'),
        ('vencida', 'Vencida'),
    ]
    
    nombre = models.CharField(max_length=200)
    organizacion_emisora = models.CharField(max_length=200)
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    descripcion = models.TextField()
    requisitos = models.JSONField()
    documentacion = models.FileField(
        upload_to='sostenibilidad/certificaciones/',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Certificación Ambiental'
        verbose_name_plural = 'Certificaciones Ambientales'
        ordering = ['-fecha_emision']
        
    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"
        
    def dias_hasta_vencimiento(self):
        if not self.fecha_vencimiento:
            return None
        from django.utils.timezone import now
        return (self.fecha_vencimiento - now().date()).days

class ObjetivoSostenibilidad(models.Model):
    CATEGORIA_CHOICES = [
        ('energia', 'Reducción de Consumo Energético'),
        ('agua', 'Optimización de Consumo de Agua'),
        ('residuos', 'Reducción de Residuos'),
        ('emisiones', 'Reducción de Emisiones'),
        ('reciclaje', 'Aumento de Reciclaje'),
    ]
    
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField()
    meta = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_objetivo = models.DateField()
    progreso_actual = models.DecimalField(max_digits=5, decimal_places=2)
    acciones_planificadas = models.TextField()
    responsable = models.ForeignKey(User, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'Objetivo de Sostenibilidad'
        verbose_name_plural = 'Objetivos de Sostenibilidad'
        ordering = ['fecha_objetivo']
        
    def __str__(self):
        return f"{self.get_categoria_display()} - {self.progreso_actual}%"
