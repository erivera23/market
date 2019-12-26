import string
import random

from django.db import models
from django.utils import timezone

from django.db.models.signals import pre_save


# Create your models here.
class CodigoPromocionalManager(models.Manager):
    def get_valid(self, codigo):
        now = timezone.now()
        return self.filter(codigo=codigo).filter(used=False).filter(valido_desde__lte=now).filter(valido_hasta__gte=now).first()

class CodigoPromocional(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.FloatField(default=0.0)
    valido_desde = models.DateTimeField()
    valido_hasta = models.DateTimeField()
    used = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CodigoPromocionalManager()

    def __str__(self):
        return self.codigo

    def use(self):
        self.used = True
        self.save()

def set_codigo(sender, instance, *args, **kwargs):
    if instance.codigo:
        return
    chars = string.ascii_uppercase + string.digits
    instance.codigo = ''.join(random.choice(chars) for _ in range(10) )

pre_save.connect(set_codigo, sender=CodigoPromocional)
