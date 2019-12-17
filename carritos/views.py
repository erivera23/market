from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrito
from .utils import get_or_create_carrito
from productos.models import Producto
from .models import CarritoProductos

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
    cantidad = int(request.POST.get('cantidad', 1))

    #carrito.productos.add(producto, through_defaults={
    #    'cantidad': cantidad
    #})

    carrito_producto = CarritoProductos.objects.create_or_update_cantidad(carrito=carrito, 
                                                                          producto=producto, 
                                                                          cantidad=cantidad)

    return render(request, 'carritos/add.html', {
        'cantidad': cantidad,
        'producto': producto
    })

def remove(request):

    carrito = get_or_create_carrito(request)
    producto = get_object_or_404(Producto, pk=request.POST.get('producto_id'))
    

    carrito.productos.remove(producto)

    return redirect('carritos:carrito')