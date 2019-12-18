from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .models import Direccion
from .forms import DireccionForm

# Create your views here.
class DireccionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = Direccion
    form_class = DireccionForm
    template_name = 'direcciones_envio/update.html'
    success_message = 'Dirección actualizada exitosamente'
    
    def get_success_url(self):
        return reverse('direcciones_envio:direcciones')

class DireccionListView(LoginRequiredMixin, ListView):
    login_url = 'login'
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