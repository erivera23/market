import uuid
import decimal
from django.db import models

from usuarios.models import User
from productos.models import Producto

from django.db.models.signals import pre_save, m2m_changed, post_save
# Create your models here.

class Carrito(models.Model):
    carrito_id = models.CharField(max_length = 100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank= True, on_delete=models.CASCADE) #uno a muchos
    productos = models.ManyToManyField(Producto, through='CarritoProductos') #Muchos a muchos
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.05 #0.5%

    def __str__(self):
        return self.carrito_id
    
    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        if self.orden:
            self.orden.update_total()

    def update_subtotal(self):
        self.subtotal = sum([ cp.cantidad * cp.producto.precio for cp in self.productos_related() ])
        self.save()

    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Carrito.FEE))
        self.save()

    def productos_related(self):
        return self.carritoproductos_set.select_related('producto')

    @property
    def orden(self):
        return self.orden_set.first()

class CarritoProductosManager(models.Manager):

    def create_or_update_cantidad(self, carrito, producto, cantidad=1):
        object, created = self.get_or_create(carrito=carrito, producto=producto)

        if not created:
            cantidad = object.cantidad + cantidad
            
        object.update_cantidad(cantidad)
        return object

class CarritoProductos(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CarritoProductosManager()

    def update_cantidad(self, cantidad=1):
        self.cantidad = cantidad
        self.save()

def set_carrito_id(sender, instance, *args, **kwargs):
    if not instance.carrito_id:
        instance.carrito_id = str(uuid.uuid4())

def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.carrito.update_totals()


pre_save.connect(set_carrito_id, sender= Carrito)
post_save.connect(post_save_update_totals, sender=CarritoProductos)
m2m_changed.connect(update_totals, sender=Carrito.productos.through)