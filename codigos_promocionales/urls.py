from django.urls import path
from . import views

app_name='codigos_promocionales'

urlpatterns = [
    path('validar', views.validate, name='validate')
]