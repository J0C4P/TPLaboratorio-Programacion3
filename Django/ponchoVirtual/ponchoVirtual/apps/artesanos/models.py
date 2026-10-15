from django.db import models
from django.db.models.deletion import CASCADE


class Artesano(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=50)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=80)
    emprendimiento = models.OneToOneField('Emprendimiento', on_delete=CASCADE, related_name="artesano")

    class Meta:
        ordering = ('nombre', )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Emprendimiento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500)
    trayectoria = models.TextField(max_length=500)
    observaciones = models.TextField(max_length=500, blank=True)
    cantidad_productos = models.IntegerField(min('1'), max('15'))
    ubicacion = models.CharField(max_length=100)

    class Meta:
        ordering = ('nombre', )

    def __str__(self):
        return f"{self.nombre}"

