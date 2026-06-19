from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Service, ServiceRequest
from .forms import ServiceRequestForm

class ServiceListView(ListView):
    model = Service
    template_name = 'cservice/services.html'
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'cservice/service_detail.html'
    context_object_name = 'service'

class ServiceRequestCreateView(CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'cservice/request.html'
    success_url = reverse_lazy('cservice:services')
