from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

from . import views
from productos.views import ProductoListView

urlpatterns = [
    path('', ProductoListView.as_view(), name='index'),
    path('usuarios/login/', views.login_view, name="login"),
    path('usuarios/logout/', views.logout_view, name="logout"),
    path('usuarios/registro/', views.register, name="register"),
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('carrito/', include('carritos.urls')),
    path('orden/', include('ordenes.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
