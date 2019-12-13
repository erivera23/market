from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Producto
# Create your views here.

class ProductoListView(ListView):
    template_name = 'index.html'
    queryset = Producto.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'

        return context

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context