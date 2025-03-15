from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
