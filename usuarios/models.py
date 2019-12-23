from django.db import models
from django.contrib.auth.models import AbstractUser
from ordenes.common import OrdenEstado
# Create your models here.

#AbstractUser o AbstractBaseUser --- 
class User(AbstractUser):
    
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def direccion_envio(self):
        return self.direccion_set.filter(default=True).first()

    def has_direccion_envio(self):
        return self.direccion_envio is not None

    def ordenes_completadas(self):
        return self.orden_set.filter(estado=OrdenEstado.COMPLETADA).order_by('-id')

class Customer(User):
    class Meta:
        proxy = True

    def get_productos(self):
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()