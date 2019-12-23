from carritos.utils import get_or_create_carrito
from .utils import get_or_create_orden

def validate_carrito_and_orden(function):
    def wrap(request, *args, **kwargs):
        carrito = get_or_create_carrito(request)
        orden = get_or_create_orden(carrito, request)
        return function(request, carrito, orden, *args, **kwargs)

    return wrap