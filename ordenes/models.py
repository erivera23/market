from enum import Enum
from django.db import models

from usuarios.models import User
from carritos.models import Carrito

# Create your models here.
class OrdenEstado(Enum):
    CREADO = 'CREADA'
    PAGADO = 'PAGADA'
    COMPLETADA = 'COMPLETADA'
    CANCELADA = 'CANCELADA'

choices = [(tag, tag.value) for tag in OrdenEstado]

class Orden(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=choices, 
                              default=OrdenEstado.CREADO) #ENum

    shipping_total = models.DecimalField(default=50, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''