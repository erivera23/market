from django.shortcuts import render, get_object_or_404, redirect
from .models import Orden
from carritos.utils import get_or_create_carrito
from .utils import get_or_create_orden, breadcrumb
from django.contrib.auth.decorators import login_required

from carritos.utils import get_or_create_carrito
from ordenes.utils import get_or_create_orden
from direcciones.models import Direccion


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

@login_required(login_url='login')
def address(request):
    carrito = get_or_create_carrito(request)
    orden = get_or_create_orden(carrito, request)
    direccion = orden.get_or_set_direccion_envio

    can_choose_direccion = request.user.direccion_set.count() > 1

    return render(request, 'ordenes/direccion.html', {
        'carrito': carrito,
        'orden': orden,
        'breadcrumb': breadcrumb(direccion=True),
        'can_choose_direccion': can_choose_direccion,
        'direccion': direccion
    })


@login_required(login_url='login')
def select_direccion(request):
    direcciones = request.user.direccion_set.all()

    return render(request,'ordenes/select_direccion.html', {
        'breadcrumb': breadcrumb(direccion=True),
        'direcciones': direcciones

    })

@login_required(login_url='login')
def check_direccion(request, pk):
    carrito = get_or_create_carrito(request)
    orden = get_or_create_orden(carrito, request)

    direccion_envio = get_object_or_404(Direccion, pk=pk)

    if request.user.id != direccion_envio.user_id:
        return redirect('carritos:carrito')

    orden.update_direccion_envio(direccion_envio)
    return redirect('ordenes:address')