from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .forms import RegistroForm

def index(request):
    return render(request, 'index.html', {
        'message': 'Listado de productos',
        'titulo': 'Productos',
        'productos': [
            {'titulo': 'Playera', 'precio': 5, 'stock': True},
            {'titulo': 'Camisa', 'precio': 7, 'stock': True},
            {'titulo': 'Mochila', 'precio': 20, 'stock': False},
            {'titulo': 'Laptop', 'precio': 200, 'stock': True}#producto
        ]
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'users/login.html', {

    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = RegistroForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('index')

    return render(request, 'users/registro.html', {
        'form': form
    })