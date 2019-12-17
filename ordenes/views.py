from django.shortcuts import render
from .models import Orden


# Create your views here.
def orden(request):
    return render(request, 'ordenes/orden.html', {
        
    })