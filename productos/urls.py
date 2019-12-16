from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('busqueda', views.ProductoBusquedaListView.as_view(), name='busqueda'),
    path('<slug:slug>', views.ProductoDetailView.as_view(), name='producto')
]