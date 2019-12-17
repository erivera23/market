from django.urls import path
from . import views
app_name = 'carritos'

urlpatterns = [
    path('', views.carrito, name='carrito'),
    path('agregar/', views.add, name='agregar'),
    path('eliminar/', views.remove, name='eliminar')
]