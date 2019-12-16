from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
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

class ProductoBusquedaListView(ListView):
    template_name = 'productos/busqueda.html'

    def get_queryset(self):
        filtros = Q(titulo__icontains=self.query()) | Q(categoria__titulo__icontains=self.query())
        # Select * from productos where titulo like %valor%
        return Producto.objects.filter(filtros)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query']= self.query()
        context['count'] = context['producto_list'].count()

        return context