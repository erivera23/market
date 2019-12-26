from django.shortcuts import render

from .models import CodigoPromocional

from django.http import JsonResponse

from carritos.utils import get_or_create_carrito
from ordenes.utils import get_or_create_orden

# Create your views here.
def validate(request):
    carrito = get_or_create_carrito(request)
    orden = get_or_create_orden(carrito, request)

    codigo = request.GET.get('code')
    promo = CodigoPromocional.objects.get_valid(codigo)

    if promo is None:
        return JsonResponse({
            'status': False
        }, status=404)
    orden.aplicar_codigo_promocion(promo)

    return JsonResponse({
        'status': True,
        'codigo': promo.codigo,
        'descuento': promo.descuento,
        'total': orden.total
    })
