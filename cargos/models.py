from django.db import models
from usuarios.models import User
from ordenes.models import Orden
from stripeAPI.cargo import create_cargo as create_cargo_stripe

# Create your models here.
class CargoManager(models.Manager):
    def create_cargo(self, orden):
        cargo = create_cargo_stripe(orden)

        return self.create(user=orden.user,
                           orden=orden,
                           cargo_id=cargo.id,
                           monto=cargo.amount,
                           metodo_pago=cargo.payment_method,
                           estado=cargo.status)

class Cargo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    cargo_id = models.CharField(max_length=50)
    monto = models.IntegerField() #Centavos
    metodo_pago=models.CharField(max_length=50) #id
    estado = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CargoManager()

    def __str__(self):
        return self.cargo_id
