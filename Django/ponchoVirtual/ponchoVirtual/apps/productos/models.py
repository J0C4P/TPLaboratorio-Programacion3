from django.db import models


class Producto(models.Model):
    categoria = models.CharField(max_length=30)
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(decimal_places=2, max_digits=10)
    localidad = models.CharField(max_length=30)
    imagen = models.FileField()
    stock = models.IntegerField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    artesano = models.ForeignKey('artesanos.Artesano', on_delete=models.CASCADE, related_name='productos_artesano')

    class Meta:
        ordering = ('categoria__nombre', )

    def __str__(self):
        return f"Producto: {self.nombre} - categoria: {self.categoria} y precio: {self.precio}"
