from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Direccion
from .forms import DireccionForm

# Create your views here.
class DireccionListView(ListView):
    model = Direccion
    template_name = 'direcciones_envio/direccion_envio.html'

    def get_queryset(self):
        return Direccion.objects.filter(user=self.request.user).order_by('-default')

@login_required(login_url='login')
def create(request):
    form = DireccionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        direccion = form.save(commit=False)
        direccion.user = request.user
        direccion.default = not Direccion.objects.filter(user=request.user).exists()

        direccion.save()
        messages.success(request, 'Dirección creada exitosamente')

        return redirect('direcciones_envio:direcciones')

    return render(request, 'direcciones_envio/create.html', {
        'form': form
    })