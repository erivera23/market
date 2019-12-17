from .models import Carrito

def get_or_create_carrito(request):
    user = request.user if request.user.is_authenticated else None
    carrito_id = request.session.get('carrito_id')
    carrito = Carrito.objects.filter(carrito_id=carrito_id).first()

    if carrito is None:
        carrito = Carrito.objects.create(user = user)

    if user and carrito.user is None:
        carrito.user = user
        carrito.save()

    request.session['carrito_id'] = carrito.carrito_id

    return carrito