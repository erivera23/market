from .models import Orden

def get_or_create_orden(carrito,request):
    orden = carrito.orden

    if orden is None and request.user.is_authenticated:
        orden = Orden.objects.create(carrito=carrito, user=request.user)
    
    if orden:
        request.session['orden_id'] = orden.orden_id

    return orden