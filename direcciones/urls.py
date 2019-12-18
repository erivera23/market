from django.urls import path
from . import views

app_name = 'direcciones_envio'

urlpatterns = [
    path('', views.DireccionListView.as_view(), name='direcciones'),
    path('nuevo/', views.create, name='create')
]