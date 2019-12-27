from django.views.generic.list import ListView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import BillingProfiles
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class BillingProfileListView(LoginRequiredMixin, ListView):
    login_url='login'
    template_name = 'billing_profiles/billing_profiles.html'

    def get_queryset(self):
        return self.request.user.billing_profiles

@login_required(login_url='login')
def create(request):

    if request.method == 'POST':
        if request.POST.get('stripeToken'):
            if not request.user.has_customer():
                request.user.create_customer_id()

            stripe_token=request.POST['stripeToken']
            billing_profile = BillingProfiles.objects.create_by_stripe_token(request.user, stripe_token)

            if billing_profile:
                messages.success(request,'Tarjeta creada exitosamente')

    return render(request, 'billing_profiles/create.html', {
        'stripe_publick_key': settings.STRIPE_PUBLIC_KEY
    })
