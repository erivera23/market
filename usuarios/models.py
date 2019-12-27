from stripeAPI.customer import create_customer
from django.db import models
from django.contrib.auth.models import AbstractUser
from ordenes.common import OrdenEstado
# Create your models here.

#AbstractUser o AbstractBaseUser --- 
class User(AbstractUser):
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def direccion_envio(self):
        return self.direccion_set.filter(default=True).first()

    @property
    def descripcion(self):
        return 'Descripción para el usuario {}'.format(self.username)
    
    def has_billing_profiles(self):
        return self.billingprofiles_set.exists()

    def has_customer(self):
        return self.customer_id is not None

    def create_customer_id(self):
        if not self.has_customer():
            customer = create_customer(self)
            self.customer_id = customer.id
            self.save()

    def has_direccion_envio(self):
        return self.direccion_envio is not None

    def ordenes_completadas(self):
        return self.orden_set.filter(estado=OrdenEstado.COMPLETADA).order_by('-id')

    def has_direcciones_envio(self):
        return self.direccion_set.exists()

    @property
    def direcciones(self):
        return self.direccion_set.all()

    @property
    def billing_profile(self):
        return self.billingprofiles_set.filter(default=True).first()

    @property
    def billing_profiles(self):
        return self.billingprofiles_set.all().order_by('-default')

class Customer(User):
    class Meta:
        proxy = True

    def get_productos(self):
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()