from django.db import models # type: ignore

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"