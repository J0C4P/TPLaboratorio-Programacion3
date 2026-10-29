from django.db import models
from django.db.models.deletion import CASCADE


class Artesano(models.Model):
    nombre_artesano = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=80)
    emprendimiento = models.OneToOneField('Emprendimiento', on_delete=CASCADE, related_name="artesano")

    class Meta:
        ordering = ('nombre_artesano', )

    def __str__(self):
        return f"{self.nombre_artesano} {self.apellido}"


class Stand(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    zona = models.CharField(max_length=50)
    artesano = models.OneToOneField('Artesano', on_delete=models.SET_NULL, null=True, blank=True, related_name='stand')

    class Meta:
        ordering = ('numero', )

    def __str__(self):
        return f"Stand {self.numero} ({self.zona})"


class Emprendimiento(models.Model):
    nombre_emprendimiento = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500)
    trayectoria = models.TextField(max_length=500)
    observaciones = models.TextField(max_length=500, blank=True)
    cantidad_productos = models.IntegerField()
    ubicacion = models.CharField(max_length=100)

    class Meta:
        ordering = ('nombre_emprendimiento', )

    def __str__(self):
        return f"{self.nombre_emprendimiento}"

