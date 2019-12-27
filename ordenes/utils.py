from django.urls import reverse
from .models import Orden


def get_or_create_orden(carrito,request):
    orden = carrito.orden

    if orden is None and request.user.is_authenticated:
        orden = Orden.objects.create(carrito=carrito, user=request.user)
    
    if orden:
        request.session['orden_id'] = orden.orden_id

    return orden

def breadcrumb(productos=True, direccion=False, pago=False, confirmacion=False):
    return [
        {'title': 'Productos', 'active': productos, 'url': reverse('ordenes:orden')},
        {'title': 'Direccion', 'active': direccion, 'url': reverse('ordenes:address')},
        {'title': 'Pago', 'active': pago, 'url': reverse('ordenes:payment')},
        {'title': 'Confirmación', 'active': confirmacion, 'url': reverse('ordenes:confirmacion')}
    ]

def destruir_orden(request):
    request.session['orden_id'] = None