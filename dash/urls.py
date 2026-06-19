from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('products/', views.DashboardProductsView.as_view(), name='products'),
    path('courses/', views.DashboardCoursesView.as_view(), name='courses'),
    path('downloads/', views.DashboardDownloadsView.as_view(), name='downloads'),
    path('invoices/', views.DashboardInvoicesView.as_view(), name='invoices'),
    path('projects/', views.DashboardProjectsView.as_view(), name='projects'),
]
