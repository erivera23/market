from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#AbstractUser o AbstractBaseUser --- 
class User(AbstractUser):
    
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Customer(User):
    class Meta:
        proxy = True

    def get_productos(self):
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()