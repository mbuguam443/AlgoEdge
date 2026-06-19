from django.views.generic import TemplateView, FormView, ListView
from django.http import JsonResponse
from .models import Testimonial, FAQ, ContactMessage
from articles.models import Newsletter

class IndexView(TemplateView):
    template_name = 'home/index.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['testimonials'] = Testimonial.objects.filter(is_featured=True)
        ctx['faqs'] = FAQ.objects.filter(is_published=True)[:6]
        return ctx

class AboutView(TemplateView):
    template_name = 'home/about.html'

class PricingView(TemplateView):
    template_name = 'home/pricing.html'

class FAQView(ListView):
    model = FAQ
    template_name = 'home/faq.html'
    context_object_name = 'faqs'
    queryset = FAQ.objects.filter(is_published=True)

def contact(request):
    from django.shortcuts import render, redirect
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            return redirect('/contact/?success=1')
    return render(request, 'home/contact.html')

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
