import uuid

from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
class Producto(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    slug = models.SlugField(null=False, blank=False, unique=True)
    imagen = models.ImageField(upload_to='productos/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    """ def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Producto, self).save(*args, **kwargs) """

    def __str__(self):
        return self.titulo

def set_slug(sender, instance, *args, **kwargs): #callback
    if instance.titulo and not instance.slug:
        
        slug = slugify(instance.titulo)
        while Producto.objects.filter(slug=slug).exists():
            
            slug = slugify(
                '{}-{}'.format(instance.titulo, str(uuid.uuid4())[:8])
            )
        instance.slug = slug

pre_save.connect(set_slug, sender=Producto)