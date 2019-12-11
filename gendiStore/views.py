from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate, login

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)

        if user:
            login(request, user)
            print("Usuario autenticado")
        else:
            print("Usuario no autenticado")
            
    return render(request, 'users/login.html', {

    })