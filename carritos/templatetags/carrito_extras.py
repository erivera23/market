from django import template

register = template.Library()

@register.filter()
def cantidad_producto_format(cantidad=1):
    return '{} {}'.format(cantidad, 'productos' if cantidad > 1 else 'producto')

@register.filter()
def cantidad_agregar_format(cantidad=1):
    return '{} {}'.format(
        cantidad_producto_format(cantidad),
        'agregados' if cantidad > 1 else 'agregado'
    )