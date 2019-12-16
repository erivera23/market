from django.db import models
from productos.models import Producto

# Create your models here.
class Categoria(models.Model):
    titulo = models.CharField(max_length = 50)
    descripcion = models.TextField()
    productos = models.ManyToManyField(Producto, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
