from django.contrib import admin
from .models import CodigoPromocional

# Register your models here.
class CodigoPromocionalAdmin(admin.ModelAdmin):
    exclude = ['codigo']

admin.site.register(CodigoPromocional, CodigoPromocionalAdmin)