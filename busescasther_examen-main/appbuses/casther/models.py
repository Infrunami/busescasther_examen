from django.contrib.auth.models import User
from django.db import models

class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    patente = models.CharField(max_length=20)
    problema = models.TextField()

    def __str__(self):
        return f"{self.modelo} ({self.patente})"

class Informe(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    reparacion = models.TextField()
    comentarios = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Informe {self.id} - {self.vehiculo}"