from enum import Enum
import uuid
import decimal
from django.db import models

from usuarios.models import User
from carritos.models import Carrito
from direcciones.models import Direccion
from codigos_promocionales.models import CodigoPromocional

from .common import OrdenEstado
from .common import choices

from django.db.models.signals import pre_save

# Create your models here.


class Orden(models.Model):
    orden_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=choices, 
                              default=OrdenEstado.CREADO) #Enum

    shipping_total = models.DecimalField(default=50, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    direccion = models.ForeignKey(Direccion, null=True, blank=True, on_delete=models.CASCADE)
    codigo_promocion = models.OneToOneField(CodigoPromocional, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.orden_id

    def aplicar_codigo_promocion(self, codigo_promocion):
        if self.codigo_promocion is None:
            self.codigo_promocion = codigo_promocion
            self.save()

            self.update_total()
            codigo_promocion.use()

    def get_or_set_direccion_envio(self):
        if self.direccion:
            return self.direccion
        direccion_envio = self.user.direccion_envio
        if direccion_envio:
            self.update_direccion_envio(direccion_envio)

        return direccion_envio
    
    def update_direccion_envio(self, direccion_envio):
        self.direccion = direccion_envio
        self.save()

    def cancel(self):
        self.estado = OrdenEstado.CANCELADA
        self.save()

    def complete(self):
        self.estado = OrdenEstado.COMPLETADA
        self.save()

    def get_total(self):
        descuento = ((decimal.Decimal(self.get_descuento())) / 100) * self.carrito.total
        return self.carrito.total + self.shipping_total - descuento

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_descuento(self):
        if self.codigo_promocion:
            return self.codigo_promocion.descuento
        return 0

def set_orden_id(sender, instance, *args, **kwargs):
    if not instance.orden_id:
        instance.orden_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_orden_id, sender=Orden)
pre_save.connect(set_total, sender=Orden)