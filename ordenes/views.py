import threading

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Orden
from carritos.utils import get_or_create_carrito
from .utils import get_or_create_orden, breadcrumb, destruir_orden
from carritos.utils import destruir_carrito
from django.contrib.auth.decorators import login_required

from carritos.utils import get_or_create_carrito
from ordenes.utils import get_or_create_orden
from direcciones.models import Direccion
from cargos.models import Cargo
from .mails import Mail
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models.query import EmptyQuerySet
from django.views.generic.list import ListView

from .decorators import validate_carrito_and_orden


# Create your views here.

class OrdenListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'ordenes/ordenes.html'

    def get_queryset(self):
        return self.request.user.ordenes_completadas()


@login_required(login_url='login')
@validate_carrito_and_orden
def orden(request, carrito, orden):
    if not carrito.has_productos():
        return redirect('carritos:carrito')
    return render(request, 'ordenes/orden.html', {
        'carrito': carrito,
        'orden': orden,
        'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
@validate_carrito_and_orden
def address(request, carrito, orden):
    if not carrito.has_productos():
        return redirect('carritos:carrito')

    direccion = orden.get_or_set_direccion_envio

    can_choose_direccion = request.user.has_direcciones_envio()

    return render(request, 'ordenes/direccion.html', {
        'carrito': carrito,
        'orden': orden,
        'breadcrumb': breadcrumb(direccion=True),
        'can_choose_direccion': can_choose_direccion,
        'direccion': direccion
    })


@login_required(login_url='login')
def select_direccion(request):
    direcciones = request.user.direcciones

    return render(request,'ordenes/select_direccion.html', {
        'breadcrumb': breadcrumb(direccion=True),
        'direcciones': direcciones

    })

@login_required(login_url='login')
@validate_carrito_and_orden
def check_direccion(request, carrito, orden, pk):

    direccion_envio = get_object_or_404(Direccion, pk=pk)

    if request.user.id != direccion_envio.user_id:
        return redirect('carritos:carrito')

    orden.update_direccion_envio(direccion_envio)
    return redirect('ordenes:address')

@login_required(login_url='login')
@validate_carrito_and_orden
def payment(request, carrito, orden):
    if not carrito.has_productos() or orden.direccion is None:
        return redirect('carritos:carrito')

    billing_profile = orden.get_or_set_billing_profile()
    return render(request, 'ordenes/payment.html', {
        'carrito': carrito,
        'orden': orden,
        'billing_profile': billing_profile,
        'breadcrumb': breadcrumb(direccion=True, pago=True)
    })

@login_required(login_url='login')
@validate_carrito_and_orden
def confirmacion(request, carrito, orden):

    if not carrito.has_productos() or orden.direccion is None or orden.billing_profile is None:
        return redirect('carritos:carrito')

    direccion = orden.direccion
    if direccion is None:
        return redirect('ordenes:address')
    
    return render(request, 'ordenes/confirmacion.html', {
        'carrito': carrito,
        'orden': orden,
        'direccion': direccion,
        'breadcrumb': breadcrumb(pago=True, direccion=True, confirmacion=True)
    })

@login_required(login_url='login')
@validate_carrito_and_orden
def cancel(request, carrito, orden):
    if request.user.id != orden.user_id:
        return redirect('carritos:carrito')

    orden.cancel()
    destruir_orden(request)
    destruir_carrito(request)

    messages.error(request, 'Orden cancelada')
    return redirect('index')

@login_required(login_url='login')
@validate_carrito_and_orden
def complete(request, carrito, orden):
    carrito = get_or_create_carrito(request)
    orden = get_or_create_orden(carrito, request)

    if request.user.id != orden.user_id:
        return redirect('carritos:carrito')
    
    cargo = Cargo.objects.create_cargo(orden)
    if cargo:
        with transaction.atomic():
            orden.complete()

            thread = threading.Thread(target=Mail.send_complete_orden, args=(
                orden, request.user
            ))
            thread.start()
            
            destruir_carrito(request)
            destruir_orden(request)

            messages.success(request, 'Compra completada exitosamente')
    return redirect('index')
