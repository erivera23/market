import uuid
from django.db import models

from usuarios.models import User
from productos.models import Producto

from django.db.models.signals import pre_save
# Create your models here.

class Carrito(models.Model):
    carrito_id = models.CharField(max_length = 100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank= True, on_delete=models.CASCADE) #uno a muchos
    productos = models.ManyToManyField(Producto) #Muchos a muchos
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.carrito_id

def set_carrito_id(sender, instance, *args, **kwargs):
    if not instance.carrito_id:
        instance.carrito_id = str(uuid.uuid4())


pre_save.connect(set_carrito_id, sender= Carrito)