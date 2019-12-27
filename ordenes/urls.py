from django.urls import path
from . import views
app_name = 'ordenes'

urlpatterns = [
    path('', views.orden, name='orden'),
    path('direccion', views.address, name='address'),
    path('seleccionar/direccion', views.select_direccion, name='select_direccion'),
    path('establecer/direccionint/<int:pk>', views.check_direccion, name='check_direccion'),
    path('confirmacion', views.confirmacion, name='confirmacion'),
    path('cancelar', views.cancel, name="cancel"),
    path('completar', views.complete, name="complete"),
    path('pago', views.payment, name='payment'),
    path('completados', views.OrdenListView.as_view(), name='completadas')
]