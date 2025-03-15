from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=32)
    is_verified = models.BooleanField(default=False)
    backup_codes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'OTP de Usuario'
        verbose_name_plural = 'OTPs de Usuarios'

    def __str__(self):
        return f'OTP para {self.user.username}'

class RegistroAuditoria(models.Model):
    ACCION_CHOICES = [
        ('crear', 'Crear'),
        ('modificar', 'Modificar'),
        ('eliminar', 'Eliminar'),
        ('login', 'Iniciar Sesión'),
        ('logout', 'Cerrar Sesión'),
        ('error', 'Error'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    objeto_afectado = GenericForeignKey('content_type', 'object_id')
    detalles = models.JSONField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    class Meta:
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.accion} por {self.usuario.username} - {self.fecha}'

class PoliticaSeguridad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor = models.JSONField()
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Política de Seguridad'
        verbose_name_plural = 'Políticas de Seguridad'

    def __str__(self):
        return self.nombre

class BackupConfiguracion(models.Model):
    FRECUENCIA_CHOICES = [
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
    ]

    nombre = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=10, choices=FRECUENCIA_CHOICES)
    hora = models.TimeField()
    ruta_destino = models.CharField(max_length=255)
    mantener_versiones = models.PositiveIntegerField()
    encriptacion_habilitada = models.BooleanField(default=True)
    notificar_error = models.BooleanField(default=True)
    ultima_ejecucion = models.DateTimeField(null=True, blank=True)
    proximo_backup = models.DateTimeField()
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Configuración de Backup'
        verbose_name_plural = 'Configuraciones de Backup'

    def __str__(self):
        return f'{self.nombre} - {self.get_frecuencia_display()}'

class Empleado(models.Model):
    TIPO_CONTRATO_CHOICES = [
        ('indefinido', 'Contrato Indefinido'),
        ('plazo_fijo', 'Plazo Fijo'),
        ('temporal', 'Temporal'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES)
    fecha_ingreso = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    certificado_manipulacion = models.FileField(
        upload_to='empleados/certificados/',
        null=True,
        blank=True
    )
    fecha_vencimiento_certificado = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['usuario__last_name', 'usuario__first_name']

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cargo}"

class Turno(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='turnos')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    area_trabajo = models.CharField(max_length=100)
    supervisor = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        related_name='turnos_supervisados'
    )
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['-fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.empleado} - {self.fecha} {self.hora_inicio}"

class Capacitacion(models.Model):
    TIPO_CHOICES = [
        ('induccion', 'Inducción'),
        ('seguridad', 'Seguridad'),
        ('calidad', 'Control de Calidad'),
        ('haccp', 'HACCP'),
        ('manipulacion', 'Manipulación de Alimentos'),
        ('tecnica', 'Capacitación Técnica'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    duracion_horas = models.PositiveIntegerField()
    instructor = models.CharField(max_length=200)
    material = models.FileField(
        upload_to='capacitaciones/material/',
        null=True,
        blank=True
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    participantes = models.ManyToManyField(
        Empleado,
        through='ParticipacionCapacitacion'
    )

    class Meta:
        verbose_name = 'Capacitación'
        verbose_name_plural = 'Capacitaciones'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class ParticipacionCapacitacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('reprobado', 'Reprobado'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    capacitacion = models.ForeignKey(Capacitacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_inscripcion = models.DateField(auto_now_add=True)
    calificacion = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )
    certificado = models.FileField(
        upload_to='capacitaciones/certificados/',
        null=True,
        blank=True
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Participación en Capacitación'
        verbose_name_plural = 'Participaciones en Capacitaciones'
        unique_together = ['empleado', 'capacitacion']

    def __str__(self):
        return f"{self.empleado} - {self.capacitacion}"
