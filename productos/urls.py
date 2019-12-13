from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.ProductoDetailView.as_view(), name='producto')
]