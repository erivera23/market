from enum import Enum
import uuid
from django.db import models

from usuarios.models import User
from carritos.models import Carrito

from django.db.models.signals import pre_save

# Create your models here.
class OrdenEstado(Enum):
    CREADO = 'CREADA'
    PAGADO = 'PAGADA'
    COMPLETADA = 'COMPLETADA'
    CANCELADA = 'CANCELADA'

choices = [(tag, tag.value) for tag in OrdenEstado]

class Orden(models.Model):
    orden_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=choices, 
                              default=OrdenEstado.CREADO) #Enum

    shipping_total = models.DecimalField(default=50, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.orden_id

    def get_total(self):
        return self.carrito.total + self.shipping_total

    def update_total(self):
        self.total = self.get_total()
        self.save()

def set_orden_id(sender, instance, *args, **kwargs):
    if not instance.orden_id:
        instance.orden_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_orden_id, sender=Orden)
pre_save.connect(set_total, sender=Orden)