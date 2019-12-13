from django.contrib import admin
from django.urls import path
from django.urls import include

from . import views
from productos.views import ProductoListView

urlpatterns = [
    path('', ProductoListView.as_view(), name='index'),
    path('usuarios/login/', views.login_view, name="login"),
    path('usuarios/logout/', views.logout_view, name="logout"),
    path('usuarios/registro/', views.register, name="register"),
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls'))
]
