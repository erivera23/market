from django.shortcuts import render
from .models import Carrito
from .utils import get_or_create_carrito
from productos.models import Producto

# Create your views here.
def carrito(request):
    #request.session['carrito_id'] = None
    carrito = get_or_create_carrito(request)

    return render(request, 'carritos/carrito.html', {
        'carrito': carrito
    })

def add(request):
    carrito = get_or_create_carrito(request)
    producto = Producto.objects.get(pk= request.POST.get('producto_id'))

    carrito.productos.add(producto)

    return render(request, 'carritos/add.html', {
        'producto': producto
    })