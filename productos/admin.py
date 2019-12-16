from django.contrib import admin
from .models import Producto
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    fields = ('titulo','descripcion', 'precio', 'imagen')
    list_display = ('__str__', 'slug', 'created_at')

admin.site.register(Producto, ProductoAdmin)