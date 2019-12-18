from django.shortcuts import render
from .models import Orden
from carritos.utils import get_or_create_carrito
from .utils import get_or_create_orden, breadcrumb
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def orden(request):
    carrito = get_or_create_carrito(request)
    orden = get_or_create_orden(carrito, request)

    return render(request, 'ordenes/orden.html', {
        'carrito': carrito,
        'orden': orden,
        'breadcrumb': breadcrumb()
    })