from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from carritos.utils import get_or_create_carrito
from ordenes.utils import get_or_create_orden

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
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
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carritos:carrito')
        return super(Direccion, self).dispatch(request, *args, **kwargs)

class DireccionListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Direccion
    template_name = 'direcciones_envio/direccion_envio.html'
    

    def get_queryset(self):
        return Direccion.objects.filter(user=self.request.user).order_by('-default')

class DireccionDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Direccion
    template_name = 'direcciones_envio/delete.html'
    success_url = reverse_lazy('direcciones_envio:direcciones')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('direcciones_envio:direcciones')
        
        if request.user.id != self.get_object().user_id:
            return redirect('direcciones_envio:direcciones')
        
        if self.get_object().has_ordenes():
            return redirect('direcciones_envio:direcciones')

        return super(DireccionDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')
def create(request):
    form = DireccionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        direccion = form.save(commit=False)
        direccion.user = request.user
        direccion.default = not request.user.has_direccion_envio()

        direccion.save()

        if request.GET.get('next'):
            if request.GET['next'] == reverse('ordenes:address'):
                carrito = get_or_create_carrito(request)
                orden = get_or_create_orden(carrito, request)
                orden.update_direccion_envio(direccion)

                return HttpResponseRedirect(request.GET['next'])
                
        messages.success(request, 'Dirección creada exitosamente')

        return redirect('direcciones_envio:direcciones')

    return render(request, 'direcciones_envio/create.html', {
        'form': form
    })

@login_required(login_url='login')
def default(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk)

    if request.user.id != direccion.user_id:
        return redirect('carritos:carrito')
    
    #Obtener antigua direccion y colocar default = False
    if request.user.has_direccion_envio():
        request.user.direccion_envio.update_default(False)
    direccion.update_default(True)

    return redirect('direcciones_envio:direcciones')