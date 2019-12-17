from django import template

register = template.Library()

@register.filter()
def precio_format(valor):
    return 'L. {0:.2f}'.format(valor)