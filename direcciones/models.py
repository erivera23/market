from django.db import models
from usuarios.models import User
# Create your models here.

class Direccion(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100)
    estado= models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    referencia = models.CharField(max_length=300)
    codigo_postal = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo_postal

    @property
    def direccion(self):
        return '{} - {} - {}'.format(self.ciudad, self.estado, self.pais)