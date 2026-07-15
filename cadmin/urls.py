from django.urls import path, include
from django.contrib.auth.models import Group
from . import views

app_name = 'cadmin'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),

    # User management (special views for auth.User)
    path('users/', views.UserListView.as_view(), name='users_list'),
    path('users/create/', views.UserCreateView.as_view(), name='users_create'),
    path('users/<int:pk>/', views.UserUpdateView.as_view(), name='users_edit'),
    path('users/<int:pk>/password/', views.UserPasswordView.as_view(), name='users_password'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='users_delete'),
]

def model_url(model, model_name, base_path):
    return [
        path(f'{base_path}/', views.ModelListView.as_view(model=model), name=f'{model_name}_list'),
        path(f'{base_path}/create/', views.ModelCreateView.as_view(model=model), name=f'{model_name}_create'),
        path(f'{base_path}/<int:pk>/', views.ModelUpdateView.as_view(model=model), name=f'{model_name}_edit'),
        path(f'{base_path}/<int:pk>/delete/', views.ModelDeleteView.as_view(model=model), name=f'{model_name}_delete'),
    ]

models_to_register = []

try:
    from django.contrib.auth.models import Group
    models_to_register.append((Group, 'group', 'roles'))
except: pass

try:
    from shop.models import Product
    models_to_register.append((Product, 'product', 'products'))
except: pass

try:
    from learn.models import Course, Lesson, Enrollment
    models_to_register.append((Course, 'course', 'academy/courses'))
    models_to_register.append((Lesson, 'lesson', 'academy/lessons'))
    models_to_register.append((Enrollment, 'enrollment', 'academy/enrollments'))
except: pass

try:
    from cservice.models import Service, ServiceRequest
    models_to_register.append((Service, 'service', 'services'))
    models_to_register.append((ServiceRequest, 'servicerequest', 'services/requests'))
except: pass

try:
    from pfarm.models import PropFirm, PropFirmChallenge
    models_to_register.append((PropFirm, 'propfirm', 'prop-firms'))
    models_to_register.append((PropFirmChallenge, 'propfirmchallenge', 'prop-firms/challenges'))
except: pass

try:
    from copytrade.models import MasterTrader, Signal, CopySubscription
    models_to_register.append((MasterTrader, 'mastertrader', 'copy-trading/traders'))
    models_to_register.append((Signal, 'signal', 'copy-trading/signals'))
    models_to_register.append((CopySubscription, 'copysubscription', 'copy-trading/subscriptions'))
except: pass

try:
    from brokerx.models import BrokerVerification, AffiliateReferral
    models_to_register.append((BrokerVerification, 'brokerverification', 'broker/verifications'))
    models_to_register.append((AffiliateReferral, 'affiliatereferral', 'broker/referrals'))
except: pass

try:
    from articles.models import Post, Category
    models_to_register.append((Post, 'post', 'blog/posts'))
    models_to_register.append((Category, 'category', 'blog/categories'))
except: pass

try:
    from userauth.models import UserProfile
    models_to_register.append((UserProfile, 'userprofile', 'profiles'))
except: pass

try:
    from refer.models import AffiliateAccount
    models_to_register.append((AffiliateAccount, 'affiliateaccount', 'referrals'))
except: pass

try:
    from automate.models import StrategyProject
    models_to_register.append((StrategyProject, 'strategyproject', 'automation/projects'))
except: pass

try:
    from alerts.models import Notification
    models_to_register.append((Notification, 'notification', 'notifications'))
except: pass

try:
    from paygate.models import Invoice, Payment, Order
    models_to_register.append((Invoice, 'invoice', 'payments/invoices'))
    models_to_register.append((Payment, 'payment', 'payments/payments'))
    models_to_register.append((Order, 'order', 'payments/orders'))
except: pass

for model, name, base in models_to_register:
    urlpatterns += model_url(model, name, base)
